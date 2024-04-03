---
title: Polymorphism
categories: [CS]
tags: [OOP, programming language theory]
image: /assets/img/previews/resized/metamon.png
math: true
---

> 부정확한 정보가 있을 수도 있습니다.
{: .prompt-info }

# Polymorphism?

다형성(Polymorphism)이란 하나의 symbol(객체, 함수, 메소드, 변수, 상수 등)이 **여러 개의 type**을 가질 수 있도록 허용하는 언어상의 특성이다.

이를 크게 4가지 종류로 구분할 수 있다.

<br />

## 1. Ad-hoc polymorphism
---
Ad-hoc polymorphism이란 하나의 함수가 다양한 종류의 parameter에 대해 동작할 수 있는 특성이다.
단, 함수는 서로 다른 parameter 종류에 대해 다르게 동작하며, 이러한 동작을 일일이 추가해 주어야 한다.
따라서 Ad-hoc이라 불리는 것이다.

~~~cpp
int add(int a, int b) {
    return a + b;
}

string add(string a, string b) {
    return a.append(b);
}
~~~
* C++의 function overloading

함수 `add`는 아래의 2가지 타입이 될 수 있다.

1. int, int -> int
2. string, string -> string

따라서 `add`는 polymorphic function이다.

<br />

## 2. Parametric polymorphism
---
Parametric polymorphism은 하나의 함수가 generic한 data type을 지닌 parameter에 대해 동작할 수 있는 특성이다.
이 경우, 함수는 parameter의 실제 type과 관계없이 동일하게 동작한다.

~~~cpp
template <typename T>
T add(T a, T b) {
    return a + b;
}
~~~
* C++에서의 function template

파라미터 `a`와 `b`는 int, float, string 등 다양한 type이 될 수 있다.
함수 `add`도 polymorphic한 parameter에 따라 여러 type을 가진다.
따라서 `add`는 (parametrically) polymorphic function이다.

<br />

## 3. Subtype polymorphism
---
임의의 type A와 B가 있다고 하자.
또한 A type의 데이터를 B type의 데이터로 치환시켜도 어느 상황에서도 어떤 식으로든 동작한다고 하자.
이 경우 B는 A의 subtype이라고 칭하며, B type의 데이터는 A type에도 함께 속한 것으로 간주할 수 있다.

Subtype polymorphism이란 이와 같이 subtyping을 구현해 데이터가 여러 개의 type을 지닐 수 있게끔 한 특성이다.

~~~cpp
class Animal {
public:
    virtual void makeSound() {
        cout << "The animal makes a sound" << endl;
    }
};

class Dog : public Animal {
public:
    void makeSound() override {
        cout << "The dog barks" << endl;
    }
};

int main() {
    Dog dog;
    Animal* animal = &dog;
    animal->makeSound();
    return 0;
}
~~~
* C++에서의 상속

Dog class는 Animal class로부터 상속받았으므로 Animal class의 인터페이스를 그대로 가진다.
따라서 Animal class의 객체는 모두 Dog class의 객체로 대체될 수 있으므로 Dog type은 Animal type의 subtype이다.

나아가 Dog class에 속한 객체 `dog`는 Dog type과 Animal type 둘 다 가진 것으로 간주되므로 polymorphic하다. 그렇기에 Animal type 포인터가 `dog`를 가리키고 있을 수 있는 것이다.

<br />

## 4. Coercion polymorphism
---
Coercion polymorphism은 특정 type과 대응하는 type conversion function을 두어 하나의 데이터가 여러개의 type으로 변환될 수 있게끔 한다. 이 역시 subtype 관계가 형성되므로 subtype polymorphism의 일종으로 볼 수 있겠지만 일반적으로 상속을 통한 subtyping만을 subtype polymorphism으로 부르는 듯 하다.

~~~cpp
class A {
public:
    operator int() {
        return 1;
    }
};

int main() {
    A a;
    int i = a;
    return 0;
}
~~~

* C++에서의 user-defined type conversion

class A의 인스턴스인 `a`는 사용자가 정의한 type conversion method으로 인해 int type으로 변환될 수 있다.
따라서 `a`는 A type과 int type을 지닌 것으로 간주되므로 polymorphic 하다.

<br />

## 보너스: subtyping vs inheritance
---
type은 객체의 interface에 집중하고, subtyping은 다형성을 통해 클래스 외부의 코드 재사용성을 높여준다.   
class는 객체의 implementation에 집중하고, inheritance는 구현의 공유를 통해 클래스 내부의 코드 재사용성을 높여준다.

* **A가 B의 subtype이라 해도, A가 B를 상속하지 않을 수도 있다.**  
파이썬의 duck typing과 C++에서의 user-defined type conversion이 그 예이다.  
또한 굳이 클래스가 아니더라도 primitive 데이터타입들 간에 subtype 관계가 있을 수 있다. Julia는 이를 명시적으로 보여주는 언어이다.

* **A가 B를 상속한다 해도 A가 B의 subtype이 아닐 수도 있다.**  
A가 B의 메소드 전체를 상속받지 않거나 일부 메소드의 parameter 혹은 return type를 다형성이 깨지도록 override하면 subtype 관계가 아니게 된다.  
예를 들어, C++의 private 상속은 superclass의 공개 메소드를 숨기므로 subtyping이 일어나지 않는다. Eiffel이나 Dart의 경우에는 메소드 override 시 parameter를 더 '자세한' type으로 변경이 가능하게끔 한다. 따라서 subtype 관계가 형성되지 않고, 만약 그래도 다형성을 보장한다면 type safe하지 않게 된다.
 
따라서 둘은 서로 독립적인 개념이다.

<br />

# 참고자료

<https://en.wikipedia.org/wiki/Polymorphism_(computer_science)>  
<https://en.wikipedia.org/wiki/Subtyping>  
<https://en.wikipedia.org/wiki/Covariance_and_contravariance_(computer_science)>  
<https://www.cs.princeton.edu/courses/archive/fall98/cs441/mainus/node12.html>