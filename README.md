# 1. 프로젝트 설명 
## 1-1) 사용 메인 라이브러리   
Python 3   
Django 3.2   
Django REST Framework 3.12   
dj-rest-auth   
django-allauth   
djangorestframework-simplejwt

## 1-2) DB 설계   
<img width="1044" alt="image" src="https://user-images.githubusercontent.com/69254943/138813175-2e5b0c84-88ce-4a5d-a5b5-d2bce9ca7062.png">   

## 1-3) 구현 설명
### A. 전체적 구조 
- Django REST Framework:   
  해당 프레임워크가 Python 기반의 Restful API 서버 구현에 가장 적합하여 사용하였습니다. 

### B. 로그인/로그아웃/회원가입      
- dj-rest-auth:   
  로그인/로그아웃/회원가입 에 대한 REST API endpoints를 제공해주는 dj-rest-auth 라이브러리를 사용하였습니다. 
- django-allauth:   
  해당 프로젝트에서는 Django의 기본 Auth User 모델을 사용하기 때문에 해당 User 모델에 대한 회원가입 구현을 위해 추가적으로 django-allauth 라이브러리를 사용하였습니다.

### C. 게시판 CRUD API & Pagination
- ModelViewSet:   
  Django REST Framework 에서 제공해주는 ModelViewSet을 사용하여 View 로직을 작성하였습니다. 
  ModelViewSet 의 경우 클래스 기반 뷰로 하나의 ViewSet 클래스로 CRUD View를 한번에 구현할 수 있어 해당 프로젝트 기능 구현을 위한 가장 간단한 방법이라고 생각하여 사용하였습니다.   
- DefaultRouter:   
  Router 를 사용해 직접 View에 대한 Url을 등록하지 않아도 자동으로 Url routing이 이루어지도록 구현하였습니다.   
- ModelSerializer:    
  Article 모델 객체을 기반으로 요청 시 들어온 데이터에 대해 검증하고 요청과 응답 시 Deserialization/Serialization 을 활용하였습니다.  
- LimitOffsetPagination:   
  Django REST Framework 에서 제공해주는 LimitOffsetPagination을 사용해 Pagination을 구현하였습니다.

### D. Authentication & Permission   
- JWT Authentication:   
  dj-rest-auth의 경우 default로 Django's Token-based authentication을 사용하지만 해당 인증 방식은 발급한 토큰을 데이터베이스에 저장하므로 비효율적입니다. 따라서 JWT authentication 구현을 위해 추가적으로 djangorestframework-simplejwt 라이브러리를 사용하였습니다.   
- AllowAny & IsOwner Permission:   
  HTTP 요청 메서드 별로 서로 다른 Permission을 적용하기 위해 APIView의 get_permissions()를 오버라이딩하였습니다.    
  - 게시물 글 목록 조회 & 특정 글 조회 : 모든 사용자가 요청 가능하도록 Django REST Framework 에서 제공해주는 AllowAny를 적용하였습니다.
  - 게시물 생성, 수정, 삭제 : Django REST Framework 에서 제공해주는 IsAuthenticated 클래스를 상속하고, 특정 게시글에 대한 수정 및 삭제 시에는 해당 게시물의 작성자만 요청 가능하도록 has_object_permission()을 추가한 IsOwner 클래스를 새롭게 생성하여 적용하였습니다.
    
---
# 2. 자세한 실행 방법 및 API 명세    
### 전체 프로젝트 실행 방법   
```
# git clone을 통해 프로젝트 코드 다운로드
git clone https://github.com/sw-develop/wecode-pre-onboarding-backend.git

# 필요 패키지 다운로드
pip install -r requirements.txt

# 로컬에서 실행
python manage.py runserver 0.0.0.0:8000
```

## PART1. 회원가입/로그인/로그아웃
### A. 회원가입
~~~Bash
POST http://127.0.0.1:8000/dj-rest-auth/registration/
~~~   

### A-1. 회원가입 성공
- Request    
~~~Bash
curl --location --request POST 'http://127.0.0.1:8000/dj-rest-auth/registration/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"test09",
    "password1":"test9999**",
    "password2":"test9999**"
}'
~~~
설명 :    
회원가입 시 사용자의 username과 비밀번호를 JSON 형태의 request body로 요청합니다.    
이때 password1과 password2는 동일해야 합니다.(동일하지 않은 경우 400 Bad Request 발생)   

- Response
~~~JSON
Status 
201 Created
 
Body
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1MjMzNDE0LCJpYXQiOjE2MzUyMzMxMTQsImp0aSI6IjMwNDdjM2MyZmRmYzQwMzA5OTE0ODNmYWMxYTI2NzEyIiwidXNlcl9pZCI6N30.bfgZGnbxcQ0mJ8pGQHPVO3BYsD9iqjoTM0dGmAvkLbY",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzNTMxOTUxNCwiaWF0IjoxNjM1MjMzMTE0LCJqdGkiOiIyYzdhMDViYjk3YzU0N2IxODg3NTg2MTg4MmYzMjQzMyIsInVzZXJfaWQiOjd9.I_z2Kkgs8Te-Fe43uW2Y9-HmwdeT8zn6EosmSsqbsdU",
    "user": {
        "pk": 7,
        "username": "test09",
        "email": "",
        "first_name": "",
        "last_name": ""
    }
}
~~~
설명 : 해당 프로젝트에서는 JWT 인증 방식을 사용하므로 해당 사용자에 대한 access_token과 refresh_token이 생성되어 반환됩니다. 또한 생성된 User 모델의 객체 정보가 반환됩니다.

### A-2. 회원가입 실패 - 이미 등록된 유저와 동일한 username인 경우
- Request   
~~~Bash
curl --location --request POST 'http://127.0.0.1:8000/dj-rest-auth/registration/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"test09",
    "password1":"test9999**",
    "password2":"test9999**"
}'
~~~
설명: Django의 기본 User 모델에서 username은 unique 제약 조건을 사용하고 있어 중복된 값이 불가능 합니다. 

- Response   
~~~JSON
Status
400 Bad Request

Body
{
    "username": [
        "A user with that username already exists."
    ]
}
~~~
설명: username 중복 시 400 Bad Request와 해당 문구가 Response로 반환됩니다.  

### B. 로그인
~~~Bash
POST  http://127.0.0.1:8000/dj-rest-auth/login/
~~~   
   
- Request   
~~~Bash
curl --location --request POST 'http://127.0.0.1:8000/dj-rest-auth/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"test09",
    "password":"test9999**"
}'
~~~
설명: 회원가입 시 등록한 username과 password를 JSON 형태의 request body에 담아 요청합니다. 

- Response   
~~~JSON
Status 
200 OK

Body
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1MjMzNTM1LCJpYXQiOjE2MzUyMzMyMzUsImp0aSI6IjM0ZDhhYWY5MjM1NDQxOTdiYmY5Y2FmM2IwZWM4OTUwIiwidXNlcl9pZCI6N30._Iu2MIHdZJFUOESmrsS9IPmr_ZIkTPxmOOW-GZNFDaw",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzNTMxOTYzNSwiaWF0IjoxNjM1MjMzMjM1LCJqdGkiOiI5MDQ2ZDAyYTE1NjQ0MmY5OWMxMDY1YWJjMjAxZDA0OSIsInVzZXJfaWQiOjd9.WxPwRJMyqk8pVHLH78VVPwCha0mrYcjxNRASNAlDEf8",
    "user": {
        "pk": 7,
        "username": "test09",
        "email": "",
        "first_name": "",
        "last_name": ""
    }
}
~~~
설명:    
해당 프로젝트는 JWT 인증 방식을 사용하므로, 로그인한 사용자에 대한 access_token과 refresh_token이 반환됩니다.    
또한 User 모델의 필드 값이 반환됩니다. 


### C. 로그아웃
~~~Bash
POST  http://127.0.0.1:8000/dj-rest-auth/logout/
~~~  

### C-1. 로그아웃 성공
- Request   
~~~Bash
curl --location --request POST 'http://127.0.0.1:8000/dj-rest-auth/logout/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1MjM0ODg3LCJpYXQiOjE2MzUyMzQ1ODcsImp0aSI6IjBjMzFhZWUyOGZjODQwMTM5MDMwODQwN2ZlOTA4YzA2IiwidXNlcl9pZCI6N30.ggj_C-P3eIJtO30qP-CJaUVl3DLpllqiowgVTmqRKp0' \
--header 'Content-Type: application/json' \
--data-raw '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzNTMyMDk4NywiaWF0IjoxNjM1MjM0NTg3LCJqdGkiOiIyZGQ3Y2QxMDQwNDg0ODQ3OGFkNWQ4MDc0NDAyMTQ2YyIsInVzZXJfaWQiOjd9.VTAFGQ_IeQrxJ4QwxhcBidVejONh6nNgAYiMlKezP-c"
}'
~~~
설명: 로그아웃 요청 시 유효한 access_token을 'Authorization: Bearer <token>'의 형태로 Authorization Header에 추가하고, 유효한 refresh_token을 JSON 형태의 request body에 담아 요청합니다. 

- Response   
~~~JSON
Status
200 OK

Body
{
    "detail": "Successfully logged out."
}
~~~
설명: 200 OK status와 '성공적으로 로그아웃 되었다'는 response body가 반환됩니다. 

### C-2. 로그아웃 실패 - 이미 로그아웃한 사용자인 경우
- Request
~~~Bash
curl --location --request POST 'http://127.0.0.1:8000/dj-rest-auth/logout/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1MjM1MzM3LCJpYXQiOjE2MzUyMzUwMzcsImp0aSI6Ijg1Yzg5NzI3ZmIwMjRhZjE4MjNhNDFmNTMxYTFlMzljIiwidXNlcl9pZCI6N30.1GSqt1Ck3Ju5oTMMuy_GJAtAj_KC6Rij2P6PCCovsIg' \
--header 'Content-Type: application/json' \
--data-raw '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzNTMyMTQzNywiaWF0IjoxNjM1MjM1MDM3LCJqdGkiOiIzMGI2YjhjN2RhOWM0ZGM2YTZlN2IyOGRhODEyY2QzYyIsInVzZXJfaWQiOjd9.MqHuwqkscvs6gT6d08cC6NIaI69s7O2IcoLhPPITxgs"
}'
~~~
설명: 로그아웃 요청 시 유효한 access_token을 'Authorization: Bearer <token>'의 형태로 Authorization Header에 추가하고, 유효한 refresh_token을 JSON 형태의 request body에 담아 요청합니다.

- Response
~~~JSON
Status
401 Unauthorized

Body
{
    "detail": "Token is blacklisted"
}
~~~
설명:    
**dj-rest-auth 라이브러리** 의 LogoutView 에서는 프로젝트의 settings 파일의 INSTALLED_APPS에 **rest_framework_simplejwt.token_blacklist** 이 추가되어 있다면, 첫 번째 로그아웃 요청 시 전달된 request body의 refresh_token을 blacklist에 추가합니다.    
따라서 이미 로그아웃한 사용자의 refresh_token을 request body에 담아 요청을 보낸다면 위의 문구와 함께 401 UnAuthorized가 발생합니다.

## PART2. 게시판 CRUD
### A. 전체 게시물 확인 with Pagination
~~~Bash
GET http://127.0.0.1:8000/api/article/?limit={value1}&offset={value2}
~~~ 

### A-1. 전체 게시물 확인 성공 (로그인한 사용자)
- Request   
~~~Bash
curl --location --request GET 'http://127.0.0.1:8000/api/article/?limit=2&offset=3' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1MjM1ODc3LCJpYXQiOjE2MzUyMzU1NzcsImp0aSI6IjFlN2JkODkwN2QyOTQxOTU5MDM3NWJmYzA3MmMxM2E5IiwidXNlcl9pZCI6N30.iLtaeOg9F9hBrmeaWqcCPBS2nNwS31bdpdzaoy8TfLA'
~~~
설명:    
로그인한 사용자의 경우 유효한 access_token을 'Authorization: Bearer <token>'의 형태로 Authorization Header에 추가하여 요청을 보내야 합니다.    
전체 게시물 조회 시 LimitOffSetPagination을 사용하므로 요청 시 Params 로 limit(반환될 instance 최대 수 = page size) & offset(시작 instance) 을 지정하여 요청합니다.

- Response   
~~~JSON
Status
200 OK

Body
{
    "count": 12,
    "next": "http://127.0.0.1:8000/api/article/?limit=2&offset=5",
    "previous": "http://127.0.0.1:8000/api/article/?limit=2&offset=1",
    "results": [
        {
            "id": 6,
            "title": "2번째 유저의 1번째 게시물 글의 제목",
            "content": "2번째 유저의 1번째 게시물 내용",
            "views": 0,
            "date_created": "2021-10-24T15:38:47.496695+09:00",
            "last_updated": "2021-10-24T15:38:47.496726+09:00",
            "user": {
                "id": 3,
                "password": "pbkdf2_sha256$260000$jZSRDz1oPPhaEdbX50Mzne$FY0+sPspOsAwNzGH9KsT7VyPDKF3eE8jS481MzErg7c=",
                "last_login": "2021-10-26T15:23:56.953851+09:00",
                "is_superuser": false,
                "username": "test03",
                "first_name": "",
                "last_name": "",
                "email": "",
                "is_staff": false,
                "is_active": true,
                "date_joined": "2021-10-24T15:37:59.056174+09:00",
                "groups": [],
                "user_permissions": []
            }
        },
        {
            "id": 7,
            "title": "2번째 유저의 2번째 게시물 글의 제목",
            "content": "2번째 유저의 2번째 게시물 내용",
            "views": 0,
            "date_created": "2021-10-24T15:45:21.390370+09:00",
            "last_updated": "2021-10-24T15:45:21.390397+09:00",
            "user": {
                "id": 3,
                "password": "pbkdf2_sha256$260000$jZSRDz1oPPhaEdbX50Mzne$FY0+sPspOsAwNzGH9KsT7VyPDKF3eE8jS481MzErg7c=",
                "last_login": "2021-10-26T15:23:56.953851+09:00",
                "is_superuser": false,
                "username": "test03",
                "first_name": "",
                "last_name": "",
                "email": "",
                "is_staff": false,
                "is_active": true,
                "date_joined": "2021-10-24T15:37:59.056174+09:00",
                "groups": [],
                "user_permissions": []
            }
        }
    ]
}
~~~
설명:    
앞서 limit=2, offset=3으로 요청을 보냈기 때문에 3번째 instance 포함 총 2개의 게시물 데이터가 반환되었음을 알 수 있습니다.    

count     : 현재 데이터베이스에 존재하는 Article 객체 수   
next      : 동일한 limit 값과 변경된 offset에 대한 요청 URL (다음 페이지)   
previous  : 동일한 limit 값과 변경된 offset에 대한 요청 URL (이전 페이지)   
result    : 반환된 게시물 객체 데이터들이고, Article 모델은 User 모델을 Foreign Key로 가지고 있는데, GET 요청에 대한 응답 Serializer 에서 depth=1로 설정하여 nested serialization 으로 처리되었습니다.   

### A-2. 전체 게시물 확인 성공 (로그인하지 않은 사용자)
- Request   
~~~Bash
curl --location --request GET 'http://127.0.0.1:8000/api/article/?limit=2&offset=3'
~~~
설명:    
전체 게시물 조회의 경우 로그인하지 않은 사용자도 요청이 가능합니다.    
전체 게시물 조회 시 LimitOffSetPagination을 사용하므로 요청 시 Params 로 limit(반환될 instance 최대 수 = page size) & offset(시작 instance) 을 지정하여 요청합니다.

- Response   
~~~JSON
Status 
200 OK

Body
{
    "count": 12,
    "next": "http://127.0.0.1:8000/api/article/?limit=2&offset=5",
    "previous": "http://127.0.0.1:8000/api/article/?limit=2&offset=1",
    "results": [
        {
            "id": 6,
            "title": "2번째 유저의 1번째 게시물 글의 제목",
            "content": "2번째 유저의 1번째 게시물 내용",
            "views": 0,
            "date_created": "2021-10-24T15:38:47.496695+09:00",
            "last_updated": "2021-10-24T15:38:47.496726+09:00",
            "user": {
                "id": 3,
                "password": "pbkdf2_sha256$260000$jZSRDz1oPPhaEdbX50Mzne$FY0+sPspOsAwNzGH9KsT7VyPDKF3eE8jS481MzErg7c=",
                "last_login": "2021-10-26T15:23:56.953851+09:00",
                "is_superuser": false,
                "username": "test03",
                "first_name": "",
                "last_name": "",
                "email": "",
                "is_staff": false,
                "is_active": true,
                "date_joined": "2021-10-24T15:37:59.056174+09:00",
                "groups": [],
                "user_permissions": []
            }
        },
        {
            "id": 7,
            "title": "2번째 유저의 2번째 게시물 글의 제목",
            "content": "2번째 유저의 2번째 게시물 내용",
            "views": 0,
            "date_created": "2021-10-24T15:45:21.390370+09:00",
            "last_updated": "2021-10-24T15:45:21.390397+09:00",
            "user": {
                "id": 3,
                "password": "pbkdf2_sha256$260000$jZSRDz1oPPhaEdbX50Mzne$FY0+sPspOsAwNzGH9KsT7VyPDKF3eE8jS481MzErg7c=",
                "last_login": "2021-10-26T15:23:56.953851+09:00",
                "is_superuser": false,
                "username": "test03",
                "first_name": "",
                "last_name": "",
                "email": "",
                "is_staff": false,
                "is_active": true,
                "date_joined": "2021-10-24T15:37:59.056174+09:00",
                "groups": [],
                "user_permissions": []
            }
        }
    ]
}
~~~
설명: 앞서 A-1과 동일합니다. 

### B. 특정 게시물 확인
~~~Bash
GET  http://127.0.0.1:8000/api/article/{article_id}/
~~~   

### B-1. 특정 게시물 확인 성공 (로그인한 사용자)
- Request   
~~~Bash
curl --location --request GET 'http://127.0.0.1:8000/api/article/9/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1MjM2NDIzLCJpYXQiOjE2MzUyMzYxMjMsImp0aSI6IjNkMzdhMzYxMGNhZTQxYWNiNDgxZGIwNzE2NWZiNGI5IiwidXNlcl9pZCI6N30.eOMacQ3FuWLeRvmCk-InvoZpayQdU_eh3cPsC9aE3-8'
~~~
설명:    
로그인한 사용자의 경우 유효한 access_token을 'Authorization: Bearer <token>'의 형태로 Authorization Header에 추가하여 요청을 보내야 합니다.    
특정 게시물의 PK(article_id) 를 URL에 추가하여야 합니다. 

- Response   
~~~JSON
Status
200 Ok

Body
{
    "id": 9,
    "title": "2번째 유저의 4번째 게시물 글의 제목",
    "content": "2번째 유저의 4번째 게시물 내용",
    "views": 1,
    "date_created": "2021-10-26T17:15:44.150753+09:00",
    "last_updated": "2021-10-26T17:15:44.150761+09:00",
    "user": {
        "id": 3,
        "password": "pbkdf2_sha256$260000$jZSRDz1oPPhaEdbX50Mzne$FY0+sPspOsAwNzGH9KsT7VyPDKF3eE8jS481MzErg7c=",
        "last_login": "2021-10-26T15:23:56.953851+09:00",
        "is_superuser": false,
        "username": "test03",
        "first_name": "",
        "last_name": "",
        "email": "",
        "is_staff": false,
        "is_active": true,
        "date_joined": "2021-10-24T15:37:59.056174+09:00",
        "groups": [],
        "user_permissions": []
    }
}

~~~
설명:    
URL에 설정한 PK(article_id) 에 해당하는 게시물 데이터가 반환됩니다.    
GET 요청에 대한 응답 Serializer 에서 depth=1로 설정하여 nested serialization 으로 처리되었습니다.   
이때 **로그인한 사용자이고 해당 게시물의 작성자가 아닌 경우** 게시물의 조회수(views)가 1씩 증가합니다.

### B-2. 특정 게시물 확인 성공 (로그인하지 않은 사용자)
- Request   
~~~Bash
curl --location --request GET 'http://127.0.0.1:8000/api/article/9/'
~~~
설명:    
특정 게시물 조회의 경우 로그인하지 않은 사용자도 가능합니다.   
특정 게시물의 PK(article_id) 를 URL에 추가하여야 합니다.

- Response   
~~~JSON
Status
200 OK

Body
{
    "id": 9,
    "title": "2번째 유저의 4번째 게시물 글의 제목",
    "content": "2번째 유저의 4번째 게시물 내용",
    "views": 2,
    "date_created": "2021-10-26T17:16:45.270776+09:00",
    "last_updated": "2021-10-26T17:16:45.270799+09:00",
    "user": {
        "id": 3,
        "password": "pbkdf2_sha256$260000$jZSRDz1oPPhaEdbX50Mzne$FY0+sPspOsAwNzGH9KsT7VyPDKF3eE8jS481MzErg7c=",
        "last_login": "2021-10-26T15:23:56.953851+09:00",
        "is_superuser": false,
        "username": "test03",
        "first_name": "",
        "last_name": "",
        "email": "",
        "is_staff": false,
        "is_active": true,
        "date_joined": "2021-10-24T15:37:59.056174+09:00",
        "groups": [],
        "user_permissions": []
    }
}
~~~
설명:   
URL에 설정한 PK(article_id) 에 해당하는 게시물 데이터가 반환됩니다.    
GET 요청에 대한 응답 Serializer 에서 depth=1로 설정하여 nested serialization 으로 처리되었습니다.   
이때 **로그인하지 않은 사용자의 경우**에는 해당 게시글의 조회수(views)가 증가하지 않습니다.   

### C. 게시물 작성
~~~Bash
 POST http://127.0.0.1:8000/api/article/
~~~   

### C-1. 게시물 작성 성공 
- Request   
~~~Bash
curl --location --request POST 'http://127.0.0.1:8000/api/article/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1MjM3NTAyLCJpYXQiOjE2MzUyMzcyMDIsImp0aSI6ImQ4MmIxMjgwYzRiZDQxMzA5NWQ2ZmRmZjQwNTFhNGZjIiwidXNlcl9pZCI6N30.8Mtn-hiaaR9xQ-Si6CmoQ7OsntnypOmjEP35ZQFlSg4' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title":"나의 2번째 게시물",
    "content":"즐거운 하루 보내세요!"
}'
~~~
설명:    
로그인한 사용자의 경우 유효한 access_token을 'Authorization: Bearer <token>'의 형태로 Authorization Header에 추가하여 요청을 보내야 합니다.   
게시물 작성 POST Serializer에서 title과 content 필드를 요청 data 값으로 설정해두었기 때문에 해당 데이터 값을 포함하여(blank도 허용하지 않음) JSON 형태의 request body로 요청을 해야 합니다. (둘 중 하나라도 포함하지 않거나, blank인 경우 400 Bad Request 발생)  

- Response   
~~~JSON
Status
201 Created

Body
{
    "title": "나의 2번째 게시물",
    "content": "즐거운 하루 보내세요!"
}
~~~
설명:
201 Created status와 JSON 형태의 response body가 반환됩니다. 

### C-2. 게시물 작성 실패 (로그인하지 않은 사용자)
- Request   
~~~Bash
curl --location --request POST 'http://127.0.0.1:8000/api/article/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title":"나의 2번째 게시물",
    "content":"즐거운 하루 보내세요!"
}'
~~~
설명: 로그인하지 않은 사용자의 경우 요청 시 Authorization Header가 포함되지 않습니다.

- Response   
~~~JSON
Status
401 Unauthorized 

Body
{
    "detail": "Authentication credentials were not provided."
}
~~~
설명: 
게시물 작성은 인증을 필요로 하므로 요청에 Authorization Header가 포함되어 있지 않거나 유효하지 않은 token 값을 포함한 경우 401 Unauthorized가 발생합니다.    

### D. 특정 게시물 수정
~~~Bash
PATCH  http://127.0.0.1:8000/api/article/{article_id}/
~~~   

### D-1. 게시물 수정 성공
- Request   
~~~Bash
curl --location --request PATCH 'http://127.0.0.1:8000/api/article/15/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1MjM3NjUyLCJpYXQiOjE2MzUyMzczNTIsImp0aSI6Ijc0N2RiOTYzYTkxMzQwZjVhNjgyNDY2ZjQ1ZWQyZDM2IiwidXNlcl9pZCI6N30.MffhkBUa040lDKPA__gWfBYHJX6Ln19Q9qHvzMe4mCg' \
--header 'Content-Type: application/json' \
--data-raw '{
    "content":"매일매일 즐거운 하루 보내세요! 수정 완료!"
}'
~~~
설명:    
로그인한 사용자의 경우 유효한 access_token을 'Authorization: Bearer <token>'의 형태로 Authorization Header에 추가하여 요청을 보내야 합니다.   
수정할 게시물의 PK(article_id) 를 URL에 추가하여 요청을 보내야 합니다.   
수정할 데이터 값을 포함하여 JSON 형태의 request body로 요청해야 합니다.    

**게시물 수정은 로그인한 사용자 본인이 작성한 게시물에 대해서만 수정이 가능합니다. (IsOwner Permission 적용)** 

- Response   
~~~JSON
Status
200 OK

Body
{
    "title": "나의 2번째 게시물",
    "content": "매일매일 즐거운 하루 보내세요! 수정 완료!"
}
~~~
설명:   
200 OK status와 수정된 값이 JSON 형태의 response body로 반환됩니다.    

### D-2. 게시물 수정 실패 (로그인한 유저 본인의 게시물이 아닌 경우)
- Request   
~~~Bash
curl --location --request PATCH 'http://127.0.0.1:8000/api/article/2/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1MjM3NjUyLCJpYXQiOjE2MzUyMzczNTIsImp0aSI6Ijc0N2RiOTYzYTkxMzQwZjVhNjgyNDY2ZjQ1ZWQyZDM2IiwidXNlcl9pZCI6N30.MffhkBUa040lDKPA__gWfBYHJX6Ln19Q9qHvzMe4mCg' \
--header 'Content-Type: application/json' \
--data-raw '{
    "content":"게시물 수정하기!!"
}'
~~~
설명:    
로그인한 사용자의 경우 유효한 access_token을 'Authorization: Bearer <token>'의 형태로 Authorization Header에 추가하여 요청을 보내야 합니다.   
수정할 게시물의 PK(article_id) 를 URL에 추가하여 요청을 보내야 합니다.   
수정할 데이터 값을 포함하여 JSON 형태의 request body로 요청해야 합니다.  

- Response   
~~~JSON
Status
403 Forbidden

Body
{
    "detail": "You do not have permission to perform this action."
}
~~~
설명:   
로그인한 사용자 본인이 작성한 게시물이 아닌 경우 해당 게시물 수정 권한이 없습니다.   
'수정 권한이 없다'는 위의 문구와 함께 403 Forbidden이 발생합니다.   

### D-3. 게시물 수정 실패 (로그인하지 않은 사용자)
- Request   
~~~Bash
curl --location --request PATCH 'http://127.0.0.1:8000/api/article/2/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "content":"게시물 수정하기!!"
}'
~~~
설명: 로그인하지 않은 사용자의 경우 요청 시 Authorization Header가 포함되지 않습니다.      

- Response   
~~~JSON
Status
401 Unauthorized

Body
{
    "detail": "Authentication credentials were not provided."
}
~~~
설명:   
게시물 수정은 로그인한 사용자 & 본인 게시물인 경우에만 가능하므로 위의 문구와 함께 401 Unauthorized가 발생합니다. 

### E. 특정 게시물 삭제
~~~Bash
DELETE  http://127.0.0.1:8000/api/article/{article_id}/
~~~   
   
### E-1. 게시물 삭제 성공
- Request   
~~~Bash
curl --location --request DELETE 'http://127.0.0.1:8000/api/article/15/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1MjM4MTUwLCJpYXQiOjE2MzUyMzc4NTAsImp0aSI6ImY4NTY5NDI3OTc0NDQyZjZiNGIwNzFlMTQxNWIwMTM2IiwidXNlcl9pZCI6N30.XkSsCXVNBoI-vufOZ0O8xgeTUbW51XiGQ3pZH3kX_rY'
~~~
설명:    
로그인한 사용자의 경우 유효한 access_token을 'Authorization: Bearer <token>'의 형태로 Authorization Header에 추가하여 요청을 보내야 합니다.   
삭제할 게시물의 PK(article_id) 를 URL에 추가하여 요청을 보내야 합니다.        

**게시물 삭제는 로그인한 사용자 본인이 작성한 게시물에 대해서만 삭제가 가능합니다. (IsOwner Permission 적용)** 

- Response   
~~~JSON
Status
204 No Content
~~~
설명:   
204 No Content가 반환되어 삭제가 정상적으로 이루어졌음을 알 수 있습니다.   

### E-2. 게시물 삭제 실패 (로그인한 유저 본인의 게시물이 아닌 경우)
- Request   
~~~Bash
curl --location --request DELETE 'http://127.0.0.1:8000/api/article/2/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1MjM4MTUwLCJpYXQiOjE2MzUyMzc4NTAsImp0aSI6ImY4NTY5NDI3OTc0NDQyZjZiNGIwNzFlMTQxNWIwMTM2IiwidXNlcl9pZCI6N30.XkSsCXVNBoI-vufOZ0O8xgeTUbW51XiGQ3pZH3kX_rY'
~~~
설명:    
로그인한 사용자의 경우 유효한 access_token을 'Authorization: Bearer <token>'의 형태로 Authorization Header에 추가하여 요청을 보내야 합니다.   
삭제할 게시물의 PK(article_id) 를 URL에 추가하여 요청을 보내야 합니다.     

- Response   
~~~JSON
Status
403 Forbidden

Body
{
    "detail": "You do not have permission to perform this action."
}
~~~
설명:   
로그인한 사용자 본인이 작성한 게시물이 아닌 경우 해당 게시물 삭제 권한이 없습니다.   
'삭제 권한이 없다'는 위의 문구와 함께 403 Forbidden이 발생합니다.

### E-3. 게시물 삭제 실패 (로그인하지 않은 사용자)
- Request   
~~~Bash
curl --location --request DELETE 'http://127.0.0.1:8000/api/article/2/'
~~~
설명: 로그인하지 않은 사용자의 경우 요청 시 Authorization Header가 포함되지 않습니다.   

- Response   
~~~JSON
Status
401 Unauthorized

Body
{
    "detail": "Authentication credentials were not provided."
}
~~~
설명: 게시물 삭제는 로그인한 사용자 & 본인 게시물인 경우에만 가능하므로 위의 문구와 함께 401 Unauthorized가 발생합니다.   

[Postman API Docs](https://documenter.getpostman.com/view/12950398/UV5cAFtM)   