[프로젝트 큰그림]

1단계 : 선수들 정보 및 경기 정보 크롤링 (csv파일) (完)

2단계 : 1차 데이터 전처리와 데이터 분석 (필요없는 컬럼들 삭제 및 상관관계 분석, 시각화를 통한 각 데이터들의 중요도 파악, 분리된 csv파일 병합)

3단계 : 정돈된 데이터들을 DB에 저장 (추후에 GUI와 연결해야 함)
	+ DB에 저장한 테이블들(선수정보, 경기정보)을 각각 join
		(선수이름을 지정하면 선수의 정보가 나오게끔)

4단계 : 머신러닝을 위한 2차 데이터 전처리 (PySpark or Python 이용)
	=> 경기정보와 선수정보를 병합
	=> 선수들의 정보들 중 파생변수나 나눠야하는 변수들 (범주형 데이터) 파악
	=> win / lose / draw 의 라벨값을 예측하는 분류모델 구축

5단계 : GUI에 만들어진 코드들을 적용 
	
	** 구현하고자 하는 최종 모습
	① 선수들의 이름을 지정하면 각 선수들의 정보를 조회해서 머신러닝에 넣고 돌림
	② 이미 학습된 머신러닝 모델이 조회된 선수들의 정보로 결과를 예측
	③ 예측된 결과를 표시 (정확도 등) 추가적으로 지정된 선수들의 정보들을 GUI에 표시 (데이터 시각화)
	
	
[역할 분담]

GUI <지수/나현> 
우선 CSV파일을 가지고 진행중인데 CSV파일안에 데이터가 NULL일때 버튼이벤트가 작동하지 않고 그냥 창이 꺼져서 해결중입니다!

Data Scientist <정범> 
- 데이터 시각화
- 복싱 선수들의 어떠한 부분을 시각화 할지 정하고 있음
- 많은 시각화 방법 중에서 어떤 방법으로 시각화를 해야 비교 및 분석이 수월할지 고민중

전처리 & 머신러닝 <서영웅>
- 각각 파일들끼리 병합하고 나서 머신러닝에 대입할 데이터전처리중
- 어떤 머신러닝을 사용할지 계속 고민중

<신엽>
-SQL 및 PySpark 문법에 익숙해지는데 해매고 있음
-웹사이트#1(BoxRec)과 웹사이트#2(BoxStats)의 데이터를 어떻게 합칠지 고민중
   - 사이트#2의 데이터는 세부적인 데이터가 많지만, 선수들의 수가 훨씬 부족함. 이를 어떻게 활용해야 할지 고민중
   - #1 #2 의 선수 데이터를 SQL상에서 합치는게 수월할지, PySpark가 편할지 고민됨. 일단 맡은 부분 전처리 하고 생각
- Python - MySQL 커넥터를 활용해서 파이썬에서 RDMBS로부터 실시간으로 데이터를 뽑아오도록 할 수 있을까?
	
