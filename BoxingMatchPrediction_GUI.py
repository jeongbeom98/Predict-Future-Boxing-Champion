# 1. File - Settings - Python Interpreter - PyMySQL / PyQt5 / PyQt5 Designer 패키지 다운 받기
# 2. 필요한 모듈 임포트 하기

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.uic import *
from matplotlib.rcsetup import validate_cycler
import pandas as pd
import pymysql.cursors
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import sklearn.metrics as mt
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import warnings
import plotly.express as px
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import os
warnings.filterwarnings('ignore')

# QT Designer에서 만든 ui불러오기
form_class = uic.loadUiType(".\\winner1.ui")[0]   #ui를 함께 올려서 경로를 바꿀 필요가 없도록 해줘야 함

# MySQL과 연동하기
cur = None
connection = pymysql.connect(host = 'database-1.cpsfn0vi5sml.ap-northeast-2.rds.amazonaws.com', user = 'root', password = 'playdata123', db = 'preprocessing', charset = 'utf8', autocommit = True, cursorclass = pymysql.cursors.DictCursor)
# connection = pymysql.connect(host = 'database-1.cpsfn0vi5sml.ap-northeast-2.rds.amazonaws.com', user = 'admin', password = 'playdata123', db = 'preprocessing', charset = 'utf8', autocommit = True, cursorclass = pymysql.cursors.DictCursor)
cur = connection.cursor()


# 기본 클래스
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resize(1400, 1000)

        ##plotly 그래프 추가한 부분

        


        # 이벤트 발생시키기
        self.ok1.clicked.connect(self.getinfo)
        self.ok2.clicked.connect(self.getinfo2)
        self.ok3.clicked.connect(self.df_ML)
        self.ok3.clicked.connect(self.show_graph) # 해당 버튼을 클릭하면 해당 함수 실행

        # comboBox : 체급, comboBox_2 : player1, comboBox_3 : player2
        self.comboBox.addItem('minimum')
        self.comboBox.addItem('light fly')
        self.comboBox.addItem('fly')
        self.comboBox.addItem('super fly')
        self.comboBox.addItem('bantam')
        self.comboBox.addItem('super bantam')
        self.comboBox.addItem('feather')
        self.comboBox.addItem('super feather')
        self.comboBox.addItem('light')
        self.comboBox.addItem('super light')
        self.comboBox.addItem('welter')
        self.comboBox.addItem('super welter')
        self.comboBox.addItem('middle')
        self.comboBox.addItem('super middle')
        self.comboBox.addItem('light heavy')
        self.comboBox.addItem('cruiser')
        self.comboBox.addItem('heavy')
        self.comboBox.activated[str].connect(lambda: self.selectedComboItem(self.comboBox))  # comboBox선택에따라 comboBox_2,comboBox_3가 바뀜

        self.comboBox_4.addItem('minimum')
        self.comboBox_4.addItem('light fly')
        self.comboBox_4.addItem('fly')
        self.comboBox_4.addItem('super fly')
        self.comboBox_4.addItem('bantam')
        self.comboBox_4.addItem('super bantam')
        self.comboBox_4.addItem('feather')
        self.comboBox_4.addItem('super feather')
        self.comboBox_4.addItem('light')
        self.comboBox_4.addItem('super light')
        self.comboBox_4.addItem('welter')
        self.comboBox_4.addItem('super welter')
        self.comboBox_4.addItem('middle')
        self.comboBox_4.addItem('super middle')
        self.comboBox_4.addItem('light heavy')
        self.comboBox_4.addItem('cruiser')
        self.comboBox_4.addItem('heavy')
        self.comboBox_4.activated[str].connect(lambda: self.selectedComboItem2(self.comboBox_4))  # comboBox선택에따라 comboBox_2,comboBox_3가 바뀜
        self.comboBox_2.addItem('체급을 선택해주세요')
        self.comboBox_3.addItem('체급을 선택해주세요')

    # def show_graph(self):
    #     df = px.data.tips()
    #     fig = px.box(df, x="day", y="total_bill", color="smoker")
    #     fig.update_traces(quartilemethod="inclusive") # or "inclusive", or "linear" by default
    #     self.plotLayout.setHtml(fig.to_html(include_plotlyjs='cdn'))   
            # 시각화와 연결시키기
    def show_graph(self):
        boxerName = [name1, name2]
        category = ['rating', 'bouts', 'KOs', 'height', 'reach', 'recent_winrate']

        preprocess_sql = 'SELECT * FROM player_info_preprocess'
        cur.execute(preprocess_sql)
        result = cur.fetchall()
        boxData =  pd.DataFrame(result) # show_figure에 사용하기 위함. 이름 필요    
       
        twoBoxers = boxData.loc[(boxData['name'].isin(boxerName)), category].reset_index()
        twoBoxers['rating']
        b1 = [twoBoxers['rating'][0], (twoBoxers['bouts'][0] / 10) * 1.3, (twoBoxers['KOs'][0] / 10),
            (twoBoxers['height'][0] / 100) * 4, (twoBoxers['reach'][0] / 100) * 4.5,
            twoBoxers['recent_winrate'][0] * 10]
        b2 = [twoBoxers['rating'][1], (twoBoxers['bouts'][1] / 10) * 1.3, (twoBoxers['KOs'][1] / 10),
            (twoBoxers['height'][1] / 100) * 4, (twoBoxers['reach'][1] / 100) * 4.5,
            twoBoxers['recent_winrate'][1] * 10]
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=b1,
            theta=category,
            fill='toself',
            name=str(boxerName[0])
        ))
        fig.add_trace(go.Scatterpolar(
            r=b2,
            theta=category,
            fill='toself',
            name=str(boxerName[1])
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=False
        )
        self.plotLayout.setHtml(fig.to_html(include_plotlyjs='cdn'))   



    # Division에 속한 선수들이 나오게 하는 함수 (Player1)
    def selectedComboItem(self, text):
        division_text = text.currentText()

        self.comboBox_2.clear()
        cur.execute("select name from player_info_gui where division = " + '\'' + f'{division_text}' + '\'' + 'order by name')
        result = cur.fetchall()
        df = pd.DataFrame(result)
        self.comboBox_2.addItems(df['name'])

    # Division에 속한 선수들이 나오게 하는 함수 (Player2)
    def selectedComboItem2(self, text):
        division_text = text.currentText()
        self.comboBox_3.clear()
        cur.execute("select name from player_info_gui where division = " + '\'' + f'{division_text}' + '\'' + 'order by name')
        result = cur.fetchall()
        df = pd.DataFrame(result)
        self.comboBox_3.addItems(df['name'])

    # player1 선택한 선수의 info를 받아오는 함수
    def getinfo(self):
        name1 = str(self.comboBox_2.currentText())

        sql = 'select * from player_info_gui where name = ' + '\'' + f'{name1}' + '\''
        cur.execute(sql)
        result = cur.fetchall()
        age_name1 = result[0]['age']
        height_name1 = result[0]['height']
        reach_name1 = result[0]['reach']
        nationality_name1 = result[0]['nationality']
        rating_name1 = result[0]['rating']
        career_name1 = result[0]['career']
        titles_name1 = result[0]['titles']
        stance_name1 = result[0]['stance']

        self.age1.setText(str(age_name1))
        self.height1.setText(str(height_name1))
        self.reach1.setText(str(reach_name1))
        self.nationality1.setText(str(nationality_name1))
        self.rating1.setText(str(rating_name1))
        self.career1.setText(str(career_name1))
        self.titles1.setText(str(titles_name1))
        self.stance1.setText(str(stance_name1))

    # player2 선택한 선수의 info를 받아오는 함수
    def getinfo2(self):
        name2 = str(self.comboBox_3.currentText())

        sql = 'select * from player_info_gui where name = ' + '\'' + f'{name2}' + '\''
        cur.execute(sql)
        result = cur.fetchall()
        age_name2 = result[0]['age']
        height_name2 = result[0]['height']
        reach_name2 = result[0]['reach']
        nationality_name2 = result[0]['nationality']
        rating_name2 = result[0]['rating']
        career_name2 = result[0]['career']
        titles_name2 = result[0]['titles']
        stance_name2 = result[0]['stance']

        self.age2.setText(str(age_name2))
        self.height2.setText(str(height_name2))
        self.reach2.setText(str(reach_name2))
        self.nationality2.setText(str(nationality_name2))
        self.rating2.setText(str(rating_name2))
        self.career2.setText(str(career_name2))
        self.titles2.setText(str(titles_name2))
        self.stance2.setText(str(stance_name2))


    # 머신러닝 코드
    def test_df(self):
        global name1, name2
        global test

        name1 = str(self.comboBox_2.currentText())  # comboBox_2에서 선택한 선수의 이름
        name2 = str(self.comboBox_3.currentText())  # comboBox_3에서 선택한 선수의 이름

        player_1_sql = 'SELECT * FROM player_info_preprocess where name = ' + '\'' + f'{name1}' + '\''  # player_info_preprocess에서 player1의 정보를 가져옴
        cur.execute(player_1_sql)
        player_1_result = cur.fetchall()
        df_1 = pd.DataFrame(player_1_result).drop(['name'], axis=1)

        player_2_sql = "SELECT * from player_info_preprocess where name = " + '\'' + f'{name2}' + '\''  # player_info_preprocess에서 player2의 정보를 가져옴
        cur.execute(player_2_sql)
        player_2_result = cur.fetchall()
        df_2 = pd.DataFrame(player_2_result).drop(['name'], axis=1)
        test = pd.concat([df_1, df_2], axis=1)  # player1과 player2의 정보를 합침

    def df_ML(self):
        self.test_df()
        sql = "SELECT * FROM boxing_merge"  # boxing_merge에서 정보를 가져옴
        cur.execute(sql)    # sql문 실행
        result = pd.DataFrame(cur.fetchall())   # sql문 실행 결과(전부)를 dataframe으로 저장
        df_features = result.drop(['date', 'player_1', 'player_2', 'match_result', 'match_rounds', 'player_1_result', 'player_2_result'], axis = 1) 
        df_label = result['player_1_result']    # player_1_result를 df_label에 저장
        encoder = LabelEncoder()        
        encoder = encoder.fit(df_label)
        df_label_encoded = encoder.transform(df_label)  # 경기 결과를 0과 1로 변환

        scaler = MinMaxScaler()
        scaler.fit(df_features)
        df_features_scaled = scaler.transform(df_features)

        X_train, X_test, y_train, y_test = train_test_split(df_features_scaled, df_label_encoded, test_size=0.3)


        xgb_model = XGBClassifier()
        xgb_model.load_model('my_model.txt')
        pred = xgb_model.predict(X_test)
        acc = mt.accuracy_score(y_test, pred)
        accuracy = '{0:.4f}'.format(acc)

        print('예측 정확도 : {0:.4f}'.format(acc))

        pred_match = xgb_model.predict(test)

        if encoder.inverse_transform(pred_match)[0] == 'W':
            match_pred = f'Winner : {name1}\n Loser : {name2}'
        elif encoder.inverse_transform(pred_match)[0] == 'L':
            match_pred = f'Winner : {name2}\n Loser : {name1}'
        elif encoder.inverse_transform(pred_match)[0] == 'D':
            match_pred = 'Draw'
        else:
            match_pred = 'Unknown Match'

        print(match_pred)

        self.accuracy11.setText(str(accuracy))
        self.result11.setText(str(match_pred))


    # 종료를 눌렀을 때 팝업창 띄우는 함수
    def closeEvent(self, QCloseEvent):

        quit_msg = "Are you sure you want to exit the program?"
        ans = QMessageBox.question(self, "Boxing Match Prediction", quit_msg,
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
