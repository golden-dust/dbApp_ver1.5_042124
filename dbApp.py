import sys
import pymysql

from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("ui/member.ui")[0]

class MainWindow(form_class, QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("회원 관리 프로그램")
        self.login_btn.clicked.connect(self.signin)
        self.loginreset_btn.clicked.connect(self.signin_reset)
        self.join_btn.clicked.connect(self.signup)
        self.joinreset_btn.clicked.connect(self.join_reset)
        self.membersearch_btn.clicked.connect(self.search_member)
        self.membermodify_btn.clicked.connect(self.modify_info)
        self.memberreset_btn.clicked.connect(self.search_reset)
        self.idcheck_btn.clicked.connect(self.check_id)
        self.delete_btn.clicked.connect(self.delete_member)
        self.deletereset_btn.clicked.connect(self.delete_reset)

        self.id_checked_ = False

    def connectDb(self):
        return pymysql.connect(user='root', password='12345', host='localhost', db='shopdb')

    def getMatchingInfo(self, field, target):
        dbConn = self.connectDb()
        sql = f"SELECT * FROM member WHERE {field} = '{target}'"
        cur = dbConn.cursor()
        cur.execute(sql)
        result = cur.fetchall()

        cur.close()
        dbConn.close()
        return result[0]

    def getSpecificInfo(self, info, field):
        if field == 'memberID':
            return info[0]
        elif field == 'memberPW':
            return info[1]
        elif field == 'memberName':
            return info[2]
        elif field == 'memberEmail':
            return info[3]
        elif field == 'memberAge':
            return info[4]

    def getAvailability(self, field, target):
        try:
            self.getMatchingInfo(field, target)
            return False
        except:
            return True


    def check_id(self):
        input_id = self.joinid_edit.text()
        if self.getAvailability("memberID", input_id):
            QMessageBox.about(self, "아이디 사용 가능", "사용 가능한 아이디입니다.")
            self.id_checked_ = True
        else:
            QMessageBox.warning(self, "아이디 사용 불가", "이미 존재하는 아이디입니다.\n새로운 아이디를 다시 입력해주세요.")

    def signup(self):
        inputID = self.joinid_edit.text()
        inputPW = self.joinpw_edit.text()
        inputName = self.joinname_edit.text()
        inputEmail = self.joinemail_edit.text()
        inputAge = self.joinage_edit.text()

        min_id_length = 5
        min_pw_length = 5
        max_id_length = 14
        max_pw_length = 20

        id_available = self.getAvailability("memberID", inputID)
        id_length_ok = (min_id_length <= len(inputID)) and (len(inputID) <= max_id_length)
        pw_length_ok = (min_pw_length <= len(inputPW)) and (len(inputPW) <= max_pw_length)
        email_available = self.getAvailability("memberEmail", inputEmail)

        if self.id_checked_ and id_available and id_length_ok and pw_length_ok and email_available:
            try:
                dbConn = self.connectDb()
                sql = f"INSERT INTO member VALUES ('{inputID}', '{inputPW}', '{inputName}', '{inputEmail}', '{inputAge}')"
                cur = dbConn.cursor()
                cur.execute(sql)
                cur.close()
                dbConn.commit()
                dbConn.close()
                QMessageBox.about(self, "회원가입성공", "축하합니다! 회원가입에 성공하였습니다.")
                self.join_reset()
            except:
                QMessageBox.warning(self, "회원가입실패", "회원가입에 실패하였습니다.")
        elif not self.id_checked_ or not id_available:
            self.id_checked_ = False
            QMessageBox.warning(self, "아이디 확인", "아이디 중복 확인을 해 주세요.")
        elif not id_length_ok:
            QMessageBox.warning(self, "아이디 길이", "아이디는 5~14자 사이여야 합니다.\n다시 입력해주세요.")
        elif not pw_length_ok:
            QMessageBox.warning(self, "비밀번호 길이", "비밀번호는 5~20자 사이여야 합니다.\n다시 입력해주세요.")
        elif not email_available:
            QMessageBox.warning(self, "중복된 이메일", "이미 등록된 이메일 주소입니다.\n다른 이메일 주소를 입력해주세요.")

    def join_reset(self):
        self.joinid_edit.clear()
        self.joinpw_edit.clear()
        self.joinname_edit.clear()
        self.joinemail_edit.clear()
        self.joinage_edit.clear()

    def search_member(self):
        inputID = self.memberid_edit.text()
        inputPW = self.memberpw_edit.text()

        try:
            info = self.getMatchingInfo("memberID", inputID)
        except:
            QMessageBox.warning(self, "조회실패", "존재하지 않는 아이디이거나 비밀번호가 잘못되었습니다.")
        else:
            pwMatch = (self.getSpecificInfo(info, "memberPW") == inputPW)
            if pwMatch:
                self.membername_edit.setText(self.getSpecificInfo(info, "memberName"))
                self.memberemail_edit.setText(self.getSpecificInfo(info, "memberEmail"))
                self.memberage_edit.setText(str(self.getSpecificInfo(info, "memberAge")))
                # 조회한 후 수정할 때는 ID는 수정하지 못하도록 ReadOnly 모드로 전환
                self.memberid_edit.setReadOnly(True)
                self.memberid_edit.setStyleSheet("color: grey;")

            else:
                QMessageBox.warning(self, "조회실패", "존재하지 않는 아이디이거나 비밀번호가 잘못되었습니다.")

    def modify_info(self):
        inputID = self.memberid_edit.text()
        inputPW = self.memberpw_edit.text()
        inputName = self.membername_edit.text()
        inputEmail = self.memberemail_edit.text()
        inputAge = self.memberage_edit.text()

        try:
            dbConn = self.connectDb()
            cur = dbConn.cursor()
            sql = f"UPDATE member SET memberPW = '{inputPW}', memberEmail = '{inputEmail}', memberName = '{inputName}', memberAge = '{inputAge}' WHERE memberID = '{inputID}'"

            cur.execute(sql)
            cur.close()
            dbConn.commit()
            dbConn.close()

            QMessageBox.about(self, "회원정보 수정 완료", "회원 정보 수정에 성공하였습니다.")
            self.search_reset()
        except:
            QMessageBox.warning(self, "회원정보 수정 실패", "회원 정보 수정에 실패하였습니다.")

    def search_reset(self):
        self.memberid_edit.clear()
        self.memberpw_edit.clear()
        self.membername_edit.clear()
        self.memberemail_edit.clear()
        self.memberage_edit.clear()

        self.memberid_edit.setReadOnly(False)
        self.memberid_edit.setStyleSheet("color: black;")

    def signin(self):
        inputID = self.loginid_edit.text()
        inputPW = self.loginpw_edit.text()

        if (inputID == "") or (inputPW == ""):
            QMessageBox.warning(self, "입력오류", "아이디와 비밀번호를 입력해주세요.")
        else:
            try:
                info = self.getMatchingInfo("memberID", inputID)
            except:
                QMessageBox.warning(self, "로그인 실패", "존재하지 않는 아이디이거나 비밀번호가 잘못되었습니다.")
            else:
                pw = info[1]
                name = info[2]
                if pw == inputPW:
                    QMessageBox.about(self, "로그인 성공", f"{name}님 환영합니다!")
                    self.signin_reset()
                else:
                    QMessageBox.warning(self, "로그인 실패", "존재하지 않는 아이디이거나 비밀번호가 잘못되었습니다.")

    def signin_reset(self):
        self.loginid_edit.clear()
        self.loginpw_edit.clear()

    def delete_member(self):
        input_id = self.deleteid_edit.text()
        input_pw = self.deletepw_edit.text()
        pw = None

        id_exists = not (self.getAvailability("memberID", input_id))
        if id_exists:
            info = self.getMatchingInfo("memberID", input_id)
            pw = info[1]

        is_pw_match = (pw == input_pw)

        if input_id == "" or input_pw == "":
            QMessageBox.warning(self, "입력오류", "탈퇴를 원하는 아이디와 비밀번호를 입력하세요.")

        elif not id_exists or not is_pw_match:
            QMessageBox.warning(self, "입력오류", "존재하지 않는 아이디거나 비밀번호가 올바르지 않습니다.")

        elif id_exists and is_pw_match:
            reply = QMessageBox.question(self, "탈퇴 확인", "정말 탈퇴하시겠습니까?", QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.No:
                self.delete_reset()
            elif reply == QMessageBox.Yes:
                try:
                    dbConn = self.connectDb()
                    cur = dbConn.cursor()
                    sql = f"DELETE FROM member WHERE memberID = '{input_id}' AND memberPW = '{input_pw}'"
                    cur.execute(sql)
                    cur.close()
                    dbConn.commit()
                    dbConn.close()
                    QMessageBox.about(self, "탈퇴 성공", "탈퇴에 성공하였습니다.")
                    self.delete_reset()
                except:
                    QMessageBox.warning(self, "탈퇴 실패", "탈퇴에 실패하였습니다.")

    def delete_reset(self):
        self.deleteid_edit.clear()
        self.deletepw_edit.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exit(app.exec_())

