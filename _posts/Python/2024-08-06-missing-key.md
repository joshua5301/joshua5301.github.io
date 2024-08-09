---
title: 딕셔너리의 키가 없을 때의 접근
categories: ['Python']
tags: ['Python']
image: /assets/img/previews/resized/python.png
math: true
---
> Effective Python의 Better way 16, 17, 18을 정리한 내용입니다.
{: .prompt-info }

## 딕셔너리로의 접근
---

가장 좋아하는 영화에 대해 투표를 받는 프로그램을 작성한다고 하자.
그럴 경우, 각 영화에 대한 투표수를 저장하는 딕셔너리가 필요할 것이다.

~~~python
movie_votes = {
    '해리포터': 3,
    '반지의 제왕': 1,
    '아이언맨': 2,
}
~~~

투표가 일어나서 딕셔너리를 변경시킬 때, 우리는 딕셔너리의 키가 존재하는지를 고려해야 한다.

<br />

## 1. 기본적인 방법
---

일반적으로, 아래와 같이 딕셔너리에 키가 있는지 명시적으로 확인 후 처리할 수 있다.

~~~python
movie = '어벤져스'

if vote in movie_votes:
    movie_votes[movie] += 1
else:
    movie_votes[movie] = 1
~~~

이 방법의 경우, 딕셔너리에 두 번 접근하고, 한 번 대입하게 된다.

다른 방법도 존재한다. 키에 먼저 접근하고, 존재하지 않는 키라 예외가 발생한다면 이 예외를 처리하는 방법이다.

~~~python
movie = '어벤져스'

try:
    movie_votes[movie] += 1
except KeyError:
    movie_votes[movie] = 1
~~~

이 방법은 이전 방법보다 효율적이다. 딕셔너리에 한 번만 접근하고, 한 번만 대입하기 때문이다.
하지만 두 방법 모두 필요 이상으로 길고 복잡해보인다.

<br />

## 2. dict.get 메소드
---

딕셔너리의 get 메소드를 사용하면 좀 더 짧고 가독성이 뛰어나게 코드를 작성할 수 있다.

~~~python 
movie = '어벤져스'

votes = movie_votes.get(movie, 0)
movie_votes[movie] = votes + 1
~~~

get의 두 번째 인자는 키가 존재하지 않을 때 가져올 default value로, 이렇게 사용했을 때 코드가 확연히 간단해졌음을 알 수 있다.
또한 예외를 처리하는 방법과 마찬가지로 딕셔너리에 한 번 접근하고 한 번 대입하게 되므로 효율적이다.

<br />

## 3. collections.defaultdict 클래스
---

dict.get 메소드 또한 상황에 따라 단점이 있을 수 있다. 
바로 default 값이 모든 경우에 생성된다는 것이다.
영화 투표의 예시를 확장시켜 영화마다 투표한 사람의 이름이 추가되도록 하자.

~~~python
movie_votes = {
    '해리포터': ['이효준', '박태지'],
    '반지의 제왕': ['신경호'],
    '아이언맨': ['곽정무'],
}
movie = '어벤져스'

vote_names = movie_votes.get(movie, [])
vote_names.append('박준하')
~~~

이 경우, 이미 존재하는 키의 경우에도 여전히 새 리스트가 생성된다. 생성되는 비용이 크다면 성능에 꽤나 영향을 미치게 될 것이다.

defaultdict 클래스는 이 상황을 쉽게 해결해 준다.

~~~python
from collections import defaultdict

movie_votes = defaultdict(list)
movie = '어벤져스'

movie_votes[movie].append('박준하')
~~~

defaultdict 클래스는 생성자에서 default 값을 생성해 줄 callable한 인자를 받는다. 이로써 defaultdict은 오직 필요할 때만 default 값을 생성하고 반환할 수 있게 된다.

<br />

## 4. \_\_missing__ 매직 메소드
---

조금 더 복잡한 상황일 때, 위 방법들로 해결할 수 없는 경우가 있다. 이때는 \_\_missing__ 매직 메소드를 사용하면 된다.

가령 영화 제목과 영화의 포스터 사진을 연결해 주는 딕셔너리를 만들고 싶다고 하자. 이 경우 default 값으로 포스터 사진을 반환하고 저장해야 한다. 

(아래 예시의 경우, 포스터의 사진 대신 이에 접근할 수 있는 핸들을 저장하고 반환하도록 하였다.)

~~~python
from collections import defaultdict

def open_picture(picture_path):
    try:
        return open(picture_path, 'rb')
    except OSError:
        print(f'경로를 열 수 없습니다. - {picture_path}')
        raise

poster_handles = defaultdict(open_picture)
handle = poster_handles['path/to/poster']
~~~

defaultdict으로 쉽게 구현할 수 있는 것 처럼 보이지만 위 예시는 실행될 수 없다. defaultdict의 default 값을 생성해 주는 팩토리는 인자를 받지 않는다는 것이다.

이처럼 default 값을 생성할 때 key에 의존해야 하는 경우에는 dict를 상속받고 \_\_missing__ 매직 메소드를 구현하자.

~~~python
class PosterHandles(dict):
    def __missing__(self, key):
        value = open_picture(key)
        self[key] = value
        return value

poster_handles = PosterHandles()
handle = poster_handles['path/to/poster']
~~~

존재하지 않는 키에 접근하려고 하면 \_\_missing__ 매직 메소드가 key 인자와 함께 호출된다. 우리는 여기서 적절한 default 값을 생성한 뒤, 저장하고 반환할 수 있다.