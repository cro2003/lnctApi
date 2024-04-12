import re
import json
import requests
from bs4 import BeautifulSoup

class accsoft:
    """This Class Contains all the Function for getting Student Accsoft information

    :arg:
        userId (str): Accsoft Identification Number given by College
        pswd (str): Password for the Accsoft Id
    """
    def __init__(self, userId: str, pswd: str):
        self.session = requests.Session()
        self.userId = userId
        self.pswd = pswd
        self.session.headers = None

    def _getLogin(self):
        if self.session.headers!=None:
            return None
        headers = {"Host": "portal.lnct.ac.in", "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"', "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": '"macOS"', "DNT": "1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Language": "en-GB,en;q=0.9", "Accept-Encoding": "gzip, deflate, br"}
        response = self.session.get("https://portal.lnct.ac.in/Accsoft2/StudentLogin.aspx", headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        viewstate = soup.find_all(id='__VIEWSTATE')[0]['value']
        viewstategenerator = soup.find_all(id='__VIEWSTATEGENERATOR')[0]['value']
        eventvalidation = soup.find_all(id='__EVENTVALIDATION')[0]['value']
        self.session.headers = {'Host': 'portal.lnct.ac.in', 'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"', 'DNT': '1', 'sec-ch-ua-mobile': '?0', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Cache-Control': 'no-cache', 'X-Requested-With': 'XMLHttpRequest', 'X-MicrosoftAjax': 'Delta=true', 'sec-ch-ua-platform': '"macOS"', 'Accept': '*/*', 'Origin': 'https://portal.lnct.ac.in', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://portal.lnct.ac.in/Accsoft2/StudentLogin.aspx', 'Accept-Language': 'en-GB,en;q=0.9', 'Cookie': f"ASP.NET_SessionId={requests.utils.dict_from_cookiejar(response.cookies)['ASP.NET_SessionId']}",}
        data = {'ctl00$ScriptManager1': 'ctl00$cph1$UpdatePanel5|ctl00$cph1$btnStuLogin', '__EVENTTARGET': '', '__EVENTARGUMENT': '', '__LASTFOCUS': '', '__VIEWSTATE': viewstate, '__VIEWSTATEGENERATOR': viewstategenerator, '__EVENTVALIDATION': eventvalidation, 'ctl00$cph1$rdbtnlType': '2', 'ctl00$cph1$hdnSID': '', 'ctl00$cph1$hdnSNO': '', 'ctl00$cph1$hdnRDURL': '', 'ctl00$cph1$txtStuUser': self.userId, 'ctl00$cph1$txtStuPsw': self.pswd, '__ASYNCPOST': 'true', 'ctl00$cph1$btnStuLogin': 'Login >>'}
        response = self.session.post('https://portal.lnct.ac.in/Accsoft2/StudentLogin.aspx', data=data)
        if BeautifulSoup(response.text, 'html.parser').find(id='ctl00_cph1_lblErrMsgStu')!=None:
            return json.dumps({"error": BeautifulSoup(response.text, 'html.parser').find(id='ctl00_cph1_lblErrMsgStu').get_text()})

    def profile(self):
        """This Function fetches profile information of the Student

        :return:
            json: Returns profile information in following format
                  {
                    "name": STUDENT_NAME,
                    "college": COLLEGE_NAME,
                    "course": COURSE,
                    "section": SECTION,
                    "enrollmentId": ENROLLMENT_NUMBER,
                    "scholarId": SCHOLAR_ID,
                    "accsoftId": ACCSOFT_ID,
                    "MobileNumber": MOBILE_NUMBER,
                    "email": EMAIL_ID,
                    "profileImage": PROFILE_IMAGE_LINK
                  }
        """
        show = self._getLogin()
        if show!=None:
            return show
        response = self.session.get('https://portal.lnct.ac.in/Accsoft2/parents/StudentPersonalDetails.aspx')
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find(id="ctl00_ContentPlaceHolder1_txtStudName")['value']
        enrollId = soup.find(id="ctl00_ContentPlaceHolder1_txtUEnrollNo")['value']
        ScholarId = soup.find(id="ctl00_ContentPlaceHolder1_txtBoardRollNo")['value']
        AccsoftId = soup.find(id="ctl00_ContentPlaceHolder1_txtEnrollNo")['value']
        course = soup.find('select', {'name': 'ctl00$ContentPlaceHolder1$drdClassNew'}).find('option', {'selected': 'selected'}).get_text()
        section = soup.find('select', {'name': 'ctl00$ContentPlaceHolder1$drdSection'}).find('option', {'selected': 'selected'}).get_text()
        MNumber = soup.find(id="ctl00_ContentPlaceHolder1_txtSMob")['value']
        email = soup.find(id="ctl00_ContentPlaceHolder1_txtSEmail")['value']
        college = soup.find("h6").get_text().strip()
        if soup.find(id="ctl00_ContentPlaceHolder1_imgphoto") == None:
            StuImage = "https://cdn.discordapp.com/attachments/1039541523311771730/1060251502389768302/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.png"
        else:
            StuImage = soup.find(id="ctl00_ContentPlaceHolder1_imgphoto")['src']
        product = {"name": name, "college": college, "course": course, "section": section, "enrollmentId": enrollId, "scholarId": ScholarId, "accsoftId": AccsoftId, "MobileNumber": MNumber, "email": email, "profileImage": StuImage}
        return json.dumps(product)

    def attendancePercentage(self):
        """This Function fetches short information on Attendace

        :return:
            json: Returns attendance information in following format
                  {
                    "name": NAME,
                    "totalLectures": TOTAL_LECTURES_HELD,
                    "present": TOTAL_LECTURES_PRESENT,
                    "absent": TOTAL_LECTURES_ABSENT,
                    "percentage": TOTAL_PERCENTAGE
                  }
        """
        show = self._getLogin()
        if show != None:
            return show
        response = self.session.get('https://portal.lnct.ac.in/Accsoft2/Parents/StuAttendanceStatus.aspx')
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find(id='ctl00_ContentPlaceHolder1_txtStudentName')['value']
        table = soup.find(id="ctl00_ContentPlaceHolder1_Gridview1")
        if table.find("td").get_text() == "Record Not Found":
            return json.dumps({"name": name, "totalLectures": 0, "present": 0, "absent": 0, "percentage": 0})
        TotalLectures = int(re.sub('\D', '', soup.find_all(id='ctl00_ContentPlaceHolder1_lbltotperiod111')[0].get_text()))
        present = int(re.sub('\D', '', soup.find_all(id='ctl00_ContentPlaceHolder1_lbltotalp11')[0].get_text()))
        absent = int(re.sub('\D', '', soup.find_all(id='ctl00_ContentPlaceHolder1_lbltotala11')[0].get_text()))
        if TotalLectures != 0:
            percentage = (present * 100 )/ TotalLectures
            percentage = round(percentage, 2)
        else:
            percentage = 0
        product = {"name": name, "totalLectures": TotalLectures, "present": present, "absent": absent, "percentage": percentage}
        return json.dumps(product)

    def attendanceDatewise(self):
        """This Function fetches Attendance of the Student Datewise

        :return:
            json: Returns datewise attendance in following format
                  {
                    "name": STUDENT_NAME,
                    "attendance": [{
                        "day": DATE,
                        "main": [{
                            "subject": SUBJECT,
                            "status": STATUS
                        }, {
                            "subject": SUBJECT,
                            "status": STATUS
                        }]
                    }, {
                        "day": DATE,
                        "main": [{
                            "subject": SUBJECT,
                            "status": STATUS
                        }, {
                            "subject": SUBJECT,
                            "status": STATUS
                        }]
                    }]
                  }
        """
        show = self._getLogin()
        if show != None:
            return show
        response = self.session.get('https://portal.lnct.ac.in/Accsoft2/Parents/StuAttendanceStatus.aspx')
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find(id='ctl00_ContentPlaceHolder1_txtStudentName')['value']
        product = {"name": name, "attendance": []}
        table = soup.find(id="ctl00_ContentPlaceHolder1_Gridview1")
        if table.find("td").get_text() == "Record Not Found":
            return json.dumps(product)
        table = table.find_all("tr")
        prevDay = None
        index = -1
        for x in table:
            new = x.find_all("td")
            if new == []: continue
            day = new[1].get_text().strip().replace('\n', '')
            subject = new[3].get_text().strip().replace('\n', '')
            status = new[4].get_text().strip().replace('\n', '')
            if day == prevDay:
                product["attendance"][index]["main"].append({"subject": subject, "status": status})
            else:
                product["attendance"].append({"day": day, "main": [{"subject": subject, "status": status}]})
                index += 1
            prevDay = day
        return json.dumps(product)

    def attendanceSubjectwise(self):
        """This Function fetches Attendance of the Student Subjectwise

                :return:
                    json: Returns subjectwise attendance in following format
                          {
                            "name": STUDENT_NAME,
                            "attendance": [{
                                "subject": SUBJECT_NAME,
                                "subShort": SHORT_NAME_SUBJECT,
                                "totalLectures": TOTAL_HELD_LECTURES,
                                "present": LECTURES_PRESENT,
                                "absent": LECTURES_ABSENT
                            }, {
                                "subject": SUBJECT_NAME,
                                "subShort": SHORT_NAME_SUBJECT,
                                "totalLectures": TOTAL_HELD_LECTURES,
                                "present": LECTURES_PRESENT,
                                "absent": LECTURES_ABSENT
                            }]
                          }
        """
        show = self._getLogin()
        if show != None:
            return show
        response = self.session.get('https://portal.lnct.ac.in/Accsoft2/parents/subwiseattn.aspx')
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find(class_='mr-2 d-none d-lg-inline small text-gray-500').get_text().strip()
        product = {"name": name, "attendance": []}
        table = soup.find(class_="mGrid")
        if table == None:
            return json.dumps(product)
        table = table.find_all("tr")
        for main in table:
            row = main.find_all('td')
            if row == []: continue
            subject = row[0].get_text()
            ssn = row[1].get_text()
            TotalLectures = int(row[2].get_text())
            AttendedLectures = int(row[3].get_text())
            product["attendance"].append({"subject": subject, "subShort": ssn, "totalLectures": TotalLectures, "present": AttendedLectures, "absent": TotalLectures - AttendedLectures})
        return json.dumps(product)

    def feeStatus(self):
        """This Function fetches Fees Information which are Paid

        :return:
            json: Returns Paid Fees information in following format
                  {
                    "name": STUDENT_NAME,
                    "feesInfo": [{
                        "txnDate": TRANSACTION_DATE,
                        "VNumber": VOUCHER_NUMBER,
                        "totalAmt": FEES_PAID
                    }, {
                        "txnDate": TRANSACTION_DATE,
                        "VNumber": VOUCHER_NUMBER,
                        "totalAmt": FEES_PAID
                    }]
                  }
        """
        show = self._getLogin()
        if show != None:
            return show
        feeSession = requests.Session()
        feeSession.headers = {'Host': 'portal.lnct.ac.in', 'Cache-Control': 'max-age=0', 'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36', 'Origin': 'https://portal.lnct.ac.in', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Referer': 'https://portal.lnct.ac.in/Accsoft2/Parents/FeesReceipts.aspx', 'Accept-Language': 'en-GB,en;q=0.9', 'Cookie': self.session.headers['Cookie'], 'Content-Type': 'application/x-www-form-urlencoded'}
        response = feeSession.get('https://portal.lnct.ac.in/Accsoft2/Parents/FeesReceipts.aspx')
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find(class_='mr-2 d-none d-lg-inline small text-gray-500').get_text().strip()
        product = {"name": name, "feesInfo": []}
        feelo = []
        for x in soup.find_all('option'):
            year = x['value']
            if soup.find(id='ctl00_ContentPlaceHolder1_VSFlexGrid1_ctl02_hdnFeeRcptID') == None:
                receiptId = None
            else:
                receiptId = soup.find(id='ctl00_ContentPlaceHolder1_VSFlexGrid1_ctl02_hdnFeeRcptID')['value']
            data = {'__EVENTTARGET': 'ctl00$ContentPlaceHolder1$ddlfinyear', '__EVENTARGUMENT': '', '__LASTFOCUS': '', '__VIEWSTATE': soup.find(id='__VIEWSTATE')['value'], '__VIEWSTATEGENERATOR': soup.find(id='__VIEWSTATEGENERATOR')['value'], '__VIEWSTATEENCRYPTED': '', '__PREVIOUSPAGE': soup.find(id='__PREVIOUSPAGE')['value'], '__EVENTVALIDATION': soup.find(id='__EVENTVALIDATION')['value'], 'ctl00$hdnCompanyID': soup.find(id='ctl00_hdnCompanyID')['value'], 'ctl00$hdnFinYearID': soup.find(id='ctl00_hdnFinYearID')['value'], 'ctl00$hdnStudentID': soup.find(id='ctl00_hdnStudentID')['value'], 'ctl00$ContentPlaceHolder1$hdnNoOfPrntCopy': soup.find(id='ctl00_ContentPlaceHolder1_hdnNoOfPrntCopy')['value'], 'ctl00$ContentPlaceHolder1$hdnrid': '', 'ctl00$ContentPlaceHolder1$ddlfinyear': year, 'ctl00$ContentPlaceHolder1$VSFlexGrid1$ctl02$hdnFeeRcptID': receiptId}
            response = feeSession.post('https://portal.lnct.ac.in/Accsoft2/Parents/FeesReceipts.aspx', data=data)
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.find(id='ctl00_ContentPlaceHolder1_VSFlexGrid1').find('td').get_text().strip() == 'There is No Record to View !':continue
            table = soup.find(id='ctl00_ContentPlaceHolder1_VSFlexGrid1')
            for z in table.find_all('tr'):
                if z.find_all('th') == []:
                    date = z.find_all('td')[2].get_text().replace('\n', '')
                    voucherNumber = z.find_all('td')[3].get_text().replace('\n', '')
                    ttlAmt = float(z.find_all('td')[4].get_text().replace('\n', ''))
                    value = {"txnDate": date, "VNumber": voucherNumber, "totalAmt": ttlAmt}
                    feelo.append(value)
        product['feesInfo'] = list(reversed(feelo))
        return json.dumps(product)

    def feetxn(self):
        """This Function fetches All the Fees Transaction which are Initiated through Accosft

        :return:
            json: Returns Online Fees Transactions in following format
                  {
                    "name": STUDENT_NAME,
                    "feetxn": [{
                        "date": TRANSACTION_DATE,
                        "paymentId": PAYMENT_ID,
                        "amount": TRANSACTION_AMOUNT,
                        "status": TRANSACTION_STATUS
                    }, {
                        "date": TRANSACTION_DATE,
                        "paymentId": PAYMENT_ID,
                        "amount": TRANSACTION_AMOUNT,
                        "status": TRANSACTION_STATUS
                    }]
                  }
        """
        show = self._getLogin()
        if show != None:
            return show
        feeSession = requests.Session()
        feeSession.headers = {'Host': 'portal.lnct.ac.in', 'Cache-Control': 'max-age=0', 'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36', 'Origin': 'https://portal.lnct.ac.in', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Referer': 'https://portal.lnct.ac.in/Accsoft2/Parents/OnlineTransactionStatus.aspx', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8', 'Cookie': self.session.headers['Cookie'], 'Content-Type': 'application/x-www-form-urlencoded'}
        response = feeSession.get('https://portal.lnct.ac.in/Accsoft2/Parents/OnlineTransactionStatus.aspx')
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find(class_='mr-2 d-none d-lg-inline small text-gray-500').get_text().strip()
        product = {"name": name, "feetxn": []}
        feelo = []
        for x in range(1,5):
            year = soup.find_all('option')[x]['value']
            data = {'__EVENTTARGET': 'ctl00$ContentPlaceHolder1$ddlfinyear', '__EVENTARGUMENT': '', '__LASTFOCUS': '', '__VIEWSTATE': soup.find(id='__VIEWSTATE')['value'], '__VIEWSTATEGENERATOR': soup.find(id='__VIEWSTATEGENERATOR')['value'], '__EVENTVALIDATION': soup.find(id='__EVENTVALIDATION')['value'], 'ctl00$hdnCompanyID': soup.find(id='ctl00_hdnCompanyID')['value'], 'ctl00$hdnFinYearID': soup.find(id='ctl00_hdnFinYearID')['value'], 'ctl00$hdnStudentID': soup.find(id='ctl00_hdnStudentID')['value'], 'ctl00$ContentPlaceHolder1$ddlfinyear': year}
            response = feeSession.post('https://portal.lnct.ac.in/Accsoft2/Parents/OnlineTransactionStatus.aspx', data=data)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find(id='ctl00_ContentPlaceHolder1_grdHistory')
            if table==None:continue
            for z in table.find_all('tr'):
                if z.find_all('th') == []:
                    date = z.find_all('td')[0].get_text().replace('\n', '')
                    pId = z.find_all('td')[1].get_text().replace('\n', '')
                    txnAmt = float(z.find_all('td')[2].get_text().replace('\n', ''))
                    status = z.find_all('td')[3].get_text().replace('\n', '')
                    value = {"date": date, "paymentId": pId, "amount": txnAmt, "status":status}
                    feelo.append(value)
        product['feetxn'] = list(reversed(feelo))
        return json.dumps(product)

    def libRecord(self):
        """This Function fetches All the Records of Issued Book from the Library

        :return:
            json: Returns Issued Book information in following format
                  {
                    "name": STUDENT_NAME,
                    "bookRecord": [{
                        "date": ISSUED_DATE,
                        "bookName": BOOK_NAME,
                        "dueDate": DUE_DATE,
                        "returnedDate": RETURNED_DATE,
                        "lateDay": LATE_DAY
                    }, {
                        "date": ISSUED_DATE,
                        "bookName": BOOK_NAME,
                        "dueDate": DUE_DATE,
                        "returnedDate": RETURNED_DATE,
                        "lateDay": LATE_DAY
                    }]
                  }
        """
        show = self._getLogin()
        if show != None:
            return show
        response = self.session.get('https://portal.lnct.ac.in/Accsoft2/Parents/CirculationLedger.aspx')
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find(class_='mr-2 d-none d-lg-inline small text-gray-500').get_text().strip()
        product = {"name": name, "bookRecord": []}
        table = soup.find(id='ctl00_ContentPlaceHolder1_grdCRList')
        if table==None:
            return json.dumps(product)
        records = []
        for x in table.find_all('tr'):
            if x.find_all('td')==[]:continue
            date = x.find_all('td')[1].get_text()
            bookName = x.find_all('td')[4].get_text()
            dueDate = x.find_all('td')[6].get_text()
            returnedDate = x.find_all('td')[7].get_text().replace('\n', '')
            lateDay = int(x.find_all('td')[8].get_text())
            value = {'date': date, 'bookName': bookName, 'dueDate': dueDate, 'returnedDate': returnedDate, 'lateDay': lateDay}
            records.append(value)
        product['bookRecord'] = records
        return json.dumps(product)

    def fineRecord(self):
        """This Function fetches All the Fine Records of the Library

        :return:
            json: Returns Fine Records in following format
                  {
                    "name": STUDENT_NAME,
                    "fine": [{
                        "libName": LIBRARY_NAME,
                        "collectedBy": FINE_COLLECTOR,
                        "date": FINE_DATE,
                        "amt": FINED_AMOUNT
                    }, {
                        "libName": LIBRARY_NAME,
                        "collectedBy": FINE_COLLECTOR,
                        "date": FINE_DATE,
                        "amt": FINED_AMOUNT
                    }]
                  }
        """
        show = self._getLogin()
        if show != None:
            return show
        response = self.session.get('https://portal.lnct.ac.in/Accsoft2/Parents/FineRecord.aspx')
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find(class_='mr-2 d-none d-lg-inline small text-gray-500').get_text().strip()
        product = {"name": name, "fine": []}
        record = []
        table = soup.find(id='ctl00_ContentPlaceHolder1_GrdFine')
        if table==None:
            return json.dumps(product)
        for x in table.find_all('tr'):
            if x.find_all('td')==[]:continue
            libName = x.find_all('td')[1].get_text()
            collectedBy = x.find_all('td')[2].get_text()
            date = x.find_all('td')[3].get_text()
            amt = float(x.find_all('td')[8].get_text())
            record.append({'libName':libName, 'collectedBy':collectedBy, 'date':date, 'amt':amt})
        product['fine'] = record
        return json.dumps(product)
