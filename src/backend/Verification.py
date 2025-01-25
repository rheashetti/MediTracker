import requests

class verification:
    def __init__(self):
        self.key = "Xa3V0z38MZVziDIidwrtwA**"

    def verify_email(self, email):
        url = f"https://globalemail.melissadata.net/v4/WEB/GlobalEmail/doGlobalEmail/?format=json&id={self.key}&email={email}&opt=VerifyMailbox:Express"
        response = requests.get(url, timeout=10)
        data = response.json()
        if data["TotalRecords"] != "0":
            return True
        
    def verify_phone(self, phone):
        url = f"https://globalphone.melissadata.net/v4/WEB/GlobalPhone/doGlobalPhone?id={self.key}&phone={phone}"
        response = requests.get(url, timeout=10)
        data = response.json()
        print(data)
        