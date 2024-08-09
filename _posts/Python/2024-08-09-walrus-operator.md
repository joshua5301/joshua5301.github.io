---
title: 왈러스 연산자
categories: ['Python']
tags: ['Python']
image: /assets/img/previews/resized/walrus.png
math: true
---
> Effective Python의 Better way 10을 정리한 내용입니다.
{: .prompt-info }

## 서론
---

생과일 주스를 파는 가게에서 과일을 보관하고 있다고 하자.
보유하고 있는 과일을 딕셔너리로 표현하면 아래와 같다.

~~~python
fruit_container = {
    '사과': 3,
    '바나나': 1,
    '포도': 2,
}
~~~

이때 손님이 와서 사과 주스를 하나 주문한다.

~~~python
fruit = '사과'
count = fruit_container.get(fruit, 0)
if count:
    juice = make_juice(fruit)
    fruit_container[fruit] = count - 1
else:
    out_of_stock()
~~~

이 코드에는 조금 아쉬운 점이 존재한다. count 변수가 정의되었지만 if 블록에서 임시로 사용되었을 뿐, 그 이후로는 사용되지 않기 때문이다. 임시 변수 치고는 변수가 너무 중요해보인다.

<br />

## 왈러스 연산자
---

왈러스 연산자(:=)는 파이썬 3.8에서 도입된 새로운 연산자로, 대입과 동시에 그 값을 사용할 수 있게 해준다. 
(한마디로, 대입문이 아니라 대입식이 된다!)

이는 위와 같은 파이썬에서의 고질적인 문제를 해결해준다.

~~~python
fruit = '사과'
if count := fruit_container.get(fruit, 0):
    juice = make_juice(fruit)
    fruit_container[fruit] = count - 1
else:
    out_of_stock()
~~~

왈러스 연산자를 사용하니 코드가 한 줄 더 짧아졌을 뿐만 아니라 count가 오직 if 블록에서만 사용된다는 것이 보여지므로 읽기 더 쉬워졌다.

> 왈러스 연산자는 연산자 우선순위가 낮다. 여러 식에 중첩하여 사용할 때는 괄호를 잊지 말자.
{: .prompt-warning }

<br />

## 또다른 예시
---

왈러스 연산자가 유용하게 사용되는 또다른 예시를 들어보겠다.

이번에는 최대한 많은 사과 주스를 만들어야 하는 상황에 놓였다고 하자.
따라서 while 루프를 통해 과일이 다 떨어질 때까지 주스를 만들도록 하였다.

~~~python
fruit = '사과'
while True:
    count = fruit_container.get(fruit, 0)
    if not count:
        break
    juice = make_juice(fruit)
    fruit_container[fruit] = count - 1
~~~

이 방식은 while 문을 단순히 무한루프로 사용하고 루프의 종료를 오직 break문에 맡긴다.
여기서 왈러스 연산자를 사용해보자.

~~~python
fruit = '사과'
while count := fruit_container.get(fruit, 0):
    juice = make_juice(fruit)
    fruit_container[fruit] = count - 1
~~~

왈러스 연산자를 사용하면 별도의 break문 없이 while 문의 표현력을 제대로 활용할 수 있게 된다.
이는 코드를 훨씬 짧고 간단하게 만든다.
