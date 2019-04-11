import unittest
import requests
import json
import datetime


class Calculator():
    def __init__(self, loanAmount, nominalRate, duration, startDate):
        self.loanAmount = loanAmount
        self.nominalRate = nominalRate
        self.duration = duration
        self.startDate = startDate

    def getJsonPostObject(self):
        payload = {"loanAmount": self.loanAmount, "nominalRate": self.nominalRate, "duration": self.duration,
                   "startDate": self.startDate}
        r = requests.post("http://localhost:8080/generate-plan", json=payload)
        data_list = json.loads(s=r.text)
        return data_list


class CalculatorUTest(unittest.TestCase):

    def setUp(self):
        self.loanAmount = "5000"
        self.nominalRate = "5.0"
        self.duration = 24
        self.startDate = "2018-05-31"
        self.calculator = Calculator(self.loanAmount, self.nominalRate, self.duration, self.startDate)
        pass

    def test_first(self):
        data = self.calculator.getJsonPostObject()
        self.assertEqual(len(data), self.duration)
        print(data[1])

    def test_second(self):
        data = self.calculator.getJsonPostObject()

        for loop in range(0, len(data) - 1):
            data_val = data[loop];
            total_sum_val = round(float(data_val['principal']) + float(data_val['interest']), 2)
            borrower_payment_amount = round(float(data_val['borrowerPaymentAmount']), 2)
            self.assertEqual(total_sum_val, borrower_payment_amount, msg="loop " + str(loop))

    def test_third(self):
        data = self.calculator.getJsonPostObject()
        is_matched = True
        for loop in range(0, len(data) - 2):
            present_month_data = data[loop]
            present_month_datetime_object = datetime.datetime.strptime(present_month_data['date'], "%Y-%m-%dT%H:%M:%SZ")
            next_month_data = data[loop + 1]
            next_month_datetime_object = datetime.datetime.strptime(next_month_data['date'], "%Y-%m-%dT%H:%M:%SZ")
            present_month_day = int(present_month_datetime_object.day)
            next_month_day = int(next_month_datetime_object.day)
            present_month_month = int(present_month_datetime_object.month)
            present_month_year = int(present_month_datetime_object.year)
            next_month_year = int(next_month_datetime_object.year)
            if present_month_month == 12:
                present_month_month = 1
                present_month_year = present_month_year + 1
            else:
                present_month_month = present_month_month + 1
            next_month_month = int(next_month_datetime_object.month)
            if present_month_day is not next_month_day \
                    and present_month_month is not next_month_month \
                    and present_month_year is not next_month_year:
                is_matched = False
                break
        self.assertTrue(is_matched)

    def test_forth(self):
        data_list = self.calculator.getJsonPostObject()
        is_matched = True
        for loop in range(0, len(data_list) - 2):
            present_month_data = data_list[loop]
            present_month_datetime_object = datetime.datetime.strptime(present_month_data['date'], "%Y-%m-%dT%H:%M:%SZ")
            next_month_data = data_list[loop + 1]
            next_month_datetime_object = datetime.datetime.strptime(next_month_data['date'], "%Y-%m-%dT%H:%M:%SZ")

            present_month_day = int(present_month_datetime_object.day)

            present_month_month = int(present_month_datetime_object.month)

            next_month_year = int(next_month_datetime_object.year)

            try:
                date_text = str(next_month_year) + "-" + str(present_month_month + 1) + "-" + str(present_month_day)
                expected_date = datetime.datetime.strptime(date_text, '%Y-%m-%d')
                if expected_date is not next_month_datetime_object:
                    is_matched = False
                    break

            except ValueError:
                present_month_month = present_month_month + 1 if present_month_day > 31 else present_month_month + 2
                present_month_day = 1 if present_month_day > 31 else present_month_day
                date_text = str(next_month_year) + "-" + str(present_month_month + 1) + "-"+ str(present_month_day)
                expected_date = datetime.datetime.strptime(date_text, '%Y-%m-%d')
                if expected_date is not next_month_datetime_object:
                    is_matched = False
                    break
                pass
        self.assertTrue(is_matched)

    def test_fifth(self):
        data_list = self.calculator.getJsonPostObject()
        is_equal = True
        for loop in range(0, len(data_list) - 1):
            data = data_list[loop]
            principal = float(data['initialOutstandingPrincipal'])
            interest = round(float(data['interest']), 2)
            calculated_interest = round(((float(self.nominalRate) * 30.00 * principal) / 360.00) / 100, 2)
            if interest != calculated_interest:
                is_equal = False
                break

        self.assertTrue(is_equal)

    # def test_sixth(self):
    #     data_list = self.calculator.getJsonPostObject()
    #     is_equal = True
    #     for loop in range(0, len(data_list) - 2):
    #         data = data_list[loop]
    #
    #         present_month_data = data_list[loop]
    #         present_month_datetime_object = datetime.datetime.strptime(present_month_data['date'], "%Y-%m-%dT%H:%M:%SZ")
    #         next_month_data = data_list[loop + 1]
    #         next_month_datetime_object = datetime.datetime.strptime(next_month_data['date'], "%Y-%m-%dT%H:%M:%SZ")
    #         date_diff = abs((next_month_datetime_object - present_month_datetime_object).days)
    #         print(date_diff)
    #         principal = float(data['initialOutstandingPrincipal'])
    #         interest = round(float(data['interest']),2)
    #         if(date_diff < 30):
    #             calculated_interest= round(((float(self.nominalRate) * date_diff * principal) / 360.00)/100,2)
    #         else:
    #             calculated_interest =round(((float(self.nominalRate) * 30.00 * principal) / 360.00)/100,2)
    #         if interest != calculated_interest:
    #             is_equal = False
    #             break
    #
    #     self.assertTrue(is_equal)

    def test_eighth(self):
        data_list = self.calculator.getJsonPostObject()
        is_equal = True
        for loop in range(0, len(data_list) - 2):
            present_month_data = data_list[loop]
            present_month_remain = float(present_month_data['remainingOutstandingPrincipal'])
            next_month_data = data_list[loop + 1]
            next_month_outstand_principal = float(next_month_data['initialOutstandingPrincipal'])
            if present_month_remain != next_month_outstand_principal:
                is_equal = False
                break

        self.assertTrue(is_equal)

    def test_ninth(self):
        data_list = self.calculator.getJsonPostObject()
        last_data = data_list[len(data_list) - 1]
        self.assertEqual(float(last_data['remainingOutstandingPrincipal']), 0.00)

    def test_tenth(self):
        data_list = self.calculator.getJsonPostObject()
        sum_principal = sum(float(item['principal']) for item in data_list)
        self.assertEqual(float(self.loanAmount), sum_principal)


if __name__ == '__main__':
    unittest.main()
