---
title: property와 descriptor
categories: ['Python']
tags: ['Python']
image: /assets/img/previews/resized/python.png
math: true
---
> Effective Python의 Better way 44, 46을 정리한 내용입니다.
{: .prompt-info }

## getter와 setter?
---

다른 언어를 사용하다 파이썬을 접한 프로그래머들은 흔히 getter와 setter 메서드를 통해 attribute에 접근하곤 한다.

~~~python
class Exam:
    def __init__(self):
        self._grade = 0

    def get_grade(self):
        return self._grade

    def set_grade(self, grade):
        if not (0 <= grade <= 100):
            raise ValueError(f'점수는 0과 100 사이여야 합니다. - 현재 점수: {grade}')
        self._grade = grade
~~~

이런 코드는 파이썬스럽지 않은데, 특히 attribute의 값을 변화시키려고 할 때 지저분해진다.

~~~python
exam = Exam()
exam.set_grade(exam.get_grade() + 1)
~~~

클래스를 구현할 때, 명시적인 getter와 setter 메서드를 구현하지 말고 일단 공개 attribute로써 시작하자.

~~~python
exam = Exam()
exam.grade += 1
~~~

그리고 만약 특별한 기능을 수행하기 위해 getter와 setter method를 설정해야 하는 상황이 왔다면, @property 데코레이터를 사용하자.

<br />

## @property 데코레이터
---

@property 데코레이터와 대응하는 setter 데코레이터는 attribute에 접근하거나 대입할 때 해당 메서드를 호출하고 getter와 setter 메서드의 역할을 대신하게끔 한다.

~~~python
class Exam:
    def __init__(self):
        self._grade = 0

    @property
    def grade(self):
        return self._grade
    
    @grade.setter
    def grade(self, grade):
        if not (0 <= grade <= 100):
            raise ValueError(f'점수는 0과 100 사이여야 합니다. - 현재 점수: {grade}')
        self._grade = grade
~~~

이러면 getter와 setter 메서드를 명시적으로 두었을 때와 달리, 정말 간편하게 attribute를 사용할 수 있다.

~~~python
exam = Exam()
exam.grade += 1
~~~

<br />

## Descriptor
---

Exam 클래스에 점수 attribute가 과목별로 여러 개 존재한다고 하자.
그렇다면 각 attribute 별로 property 데코레이터를 사용해 getter와 setter 메서드를 구현해야 할 것이다.

~~~python
class Exam:
    def __init__(self):
        self._math_grade = 0
        self._writing_grade = 0
        self._science_grade = 0

    @property
    def math_grade(self):
        return self._math_grade

    @property
    def writing_grade(self):
        return self._writing_grade
    
    ...
    (이하 생략)
~~~

이런 식으로 일일이 확장한다면 읽는 사람도 쓰는 사람도 매우 번거로울 수밖에 없다.
다행히 descriptor를 사용하면 이렇게 중복되는 property의 로직을 쉽게 재사용할 수 있다.

Descriptor class의 \_\_get__ 메서드와 \_\_set__ 메서드에 getter와 setter의 로직을 구현하고, 이의 instance를 클래스 attribute로 두면 쉽게 재사용가능한 property가 완성된다.

~~~python
class Grade:
    def __get__(self, instance, instance_type):
        ...
    def __set__(self, instance, value):
        ...

class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()
~~~

Descriptor는 class attribute로, class 별로 오직 하나의 인스턴스만이 존재한다.
따라서 attribute로 단순히 반환해야할 값을 보관하는 것이 아닌, 메서드를 호출한 instance 별로 반환해야할 값을 저장한 dictionary를 보관해야 한다.

~~~python
from weakref import WeakKeyDictionary

class Grade:
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError(f'점수는 0과 100 사이여야 합니다. - 현재 점수: {grade}')
        self._values[instance] = value
~~~

특히 유의할 점은, 이 딕셔너리를 일반 딕셔너리가 아닌 weak reference를 유지하는 딕셔너리로 두어야 한다는 것이다.
만약 strong reference를 유지하는 일반 딕셔너리로 인스턴스를 key로 저장하게 되면, 이 인스턴스는 영원히 그 딕셔너리에 묶여있어 garbage collector가 메모리를 수집할 수 없다. Memory leak가 일어난다는 것이다.

따라서 garbage collector가 제대로 메모리를 수집할 수 있도록 weakref 모듈의 WeakKeyDictionary 클래스를 사용하자.