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

[전처리]

- 데이터 전처리 (컬럼별)
- residence : 나라만 저장
- ID는 정수로 하면 머신러닝때 영향을 끼칠 수 있기 때문에 str타입으로 변경(머신러닝때는 drop 예정)
- rating : int로 변환하고 총인원 중 몇 %에 위치하는지 계산 & 아래에 몇명이 있는지로 변환 (e.g 수능 성적 받으면 1등급은 백분위 수가 96으로 되어있는것과 동일한 원리)
- reach와 height는 단위를 제거하고 int값으로 변환
- KOs : 단위값 제거하고 float으로 변환
- career : career가 0이면 일단 debut의 연도와 현재 연도를 빼서 career를 구함 => debut 컬럼은 필요없으니 drop
- titles, age : int로 형변환
- division
- 미니멈, 라이트플라이, 플라이, 슈퍼플라이 : 1
- 밴텀, 슈퍼밴텀, 페더, 슈퍼페터 : 2
- 라이트, 슈퍼라이트, 웰터, 슈퍼웰터 : 3
- 미들, 슈퍼미들, 라이트헤비 : 4
- 크루저, 헤비 : 5
- nationality, residence 둘중 하나라도 밑의 리스트에 존재하면
- li1 = ['USA', 'Mexico', 'United Kingdom'] => 3
- li2 = ['Russia', 'Japan', 'Ukraine', 'Philippines'] => 2
- li3 = ['Cuba', 'South Africa', 'Argentina'] => 1
- 해당 plus_point로 변환
- stance는 OneHotEncoding으로 orthodox / southpaw / unknown_position 으로 존재하면 1, 존재하지 않으면 0으로 인코딩 후 stance 컬럼 drop
- 머신러닝을 위해서 object 형태인 컬럼들을 int or float 으로 형변환 해줌
	
10/05 수정점 <신엽>
- 시각화가 GUI에서 출력되도록 함
   - 이 부분에서 사용된 plotly는 html이 있어야 동작하는 부분이라, 그래프가 출력되는 위젯을 웹 브라우저로 대체하여 넣었습니다.
- DB에서 데이터를 받아와서 사용하도록 함
   - 로컬에 데이터가 존재해야 동작하던 것을 AWS DB에서 직접 데이터를 쿼리해와서 사용하도록 수정하였습니다.
- 머신러닝 모델을 외부에 저장해두고, 불러와서 사용하도록 함
   - <Start Matching>버튼을 누를 때 마다 새로 학습이 진행되던 것을, xgboost모델을 저장해두고 불러와서 predict만 하도록 수정했습니다. 속도 향상이 있었습니다.

추후 개선점
- .py파일을 .exe파일로 변경
   - 파이썬이 없는 환경에서도 돌아가도록 .exe파일로 변환해보려고 합니다
   - 다만 몇 가지 에러로 인해 막혀있습니다. 추후 해 볼 예정입니다.
- 결측치 전처리
   - reach, height등 결측치가 상당히 많습니다. 
   - 이 부분을 비슷한 조건의 선수들의 평균으로 채워 넣는다던지 해서 재학습/재예측 하면 좋을 것 같습니다.
   - 다만 이 부분은 동기부여가 약해서 굳이 안 할 것 같긴 합니다.

후기
- 다들 고생 많으셨습니다. 정리 작업이 걸리는 문제가 많아 예정보다 많이 늦어졌네요.
개인적으로 여기서 더 작업하면 더 좋은 결과물을 낼 수 있을 것 같다는 아쉬움이 있긴 합니다. 
하지만 프로젝트 일정도 끝났고 각자의 스케줄이 있으니 이 정도에서 끊어야 할 것 같습니다. 

다들 각자의 역할을 맡아주신다고 고생 많으셨습니다. 특히 많은 부분을 담당하신 영웅님께 감사드립니다.
