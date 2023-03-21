# ETL 파이프라인 구축 프로젝트

## 아키텍처 
![스크린샷 2023-03-21 오전 9 04 27](https://user-images.githubusercontent.com/112758969/226512550-6acb0468-8033-4c7f-953b-8964da09312e.png)

## 구성
- [파이프라인 코드](https://github.com/physedsnu/AI-etl-pipeline/blob/main/pipeline.py) : 추출-변환-적재 자동화 코드
- [api로그 및 압축 파일 예시](https://github.com/physedsnu/AI-etl-pipeline/tree/main/example) : 변환전, 변환 후 
- [스케줄링 명령어](https://github.com/physedsnu/AI-etl-pipeline/blob/main/crontab.txt) : 로컬에서 진행 (AWS경우 CloudWatch 이벤트규칙 → 일정에서 cron식 입력)


## 결과 

![스크린샷 2023-03-21 오전 9 40 59](https://user-images.githubusercontent.com/112758969/226513167-663c05ce-152a-4563-8505-5b4cd2185fdf.png)
![스크린샷 2023-03-21 오전 10 15 06](https://user-images.githubusercontent.com/112758969/226513175-44cf8ab2-7b55-4e75-9421-a1c7e00fac79.png)

## 클린업 
crontab 초기화 : 로그가 계속 쌓여 과금 되는 것 방지 
```
$ crontab -r 
$ crontab -l
no crontab for ubuntu
```
