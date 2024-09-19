# SolarEMS_Web
$ git config --global user.name "작성자 이름"  <br>
$ git config --global user.email "작성자 이메일" <br><br>

밑에 설명들은 다 cmd 창에서 하는 거에용
## cmd창을 이용하여 가상환경을 열고, 실행하기(건 전용 방법)

 	1. D드라이브로 이동<br>
  		$ cd/d D:\ <br><br>

 	2. github 폴더에 있는 프로젝트 파일로 이동 <br>
  		$ cd github <br>
		$ cd SolarEMS_Web <br><br>

  	3. 가상환경 연결하기 <br>
   		$ venv\Scripts\activate.bat <br><br>

 	4. 프로젝트 실행하기 <br>
  		$ python manage.py runserver <br><br>


## git hub 업데이트 하는 방법 (Commit 방법)
  
  1. 업데이트 할 파일을 선택하여 add해준다.<br>
     $ git add 파일이름  <br>
     $ git add . (전체 업데이트 할때)<br><br>
   
 
	
  2. add 했던 것을 commit 해주는 명령어<br>
     $ git commit -m "입력할 메세지" (commit에 대한 설명을 해주는)<br><br>


  3. 생성한 커밋 확인 코드<br>
     $ git log (작성자, 이메일, 작성시간 뜬다고 하네용)<br>
     (나가는 방법은 q버튼!)<br><br>


  4. 저장소에 올려주기<br>
     $ git push (commit된 변경사항만 로컬 저장소에 저장될거에요)<br><br>

## 강제 푸시 / 강제 덮어쓰기 

[git hub 강제 푸시]<br>
git add . <br>
git commit -m "다시한번 올린다." <br>
git push --force origin main <br><br>

[git hub 강제 덮어쓰기] <br>
git fetch origin <br>
git reset --hard origin/main <br>
