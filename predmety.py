from bs4 import BeautifulSoup
import requests, os, time

def main():
  login_url = "https://vzdelavanie.uniza.sk/vzdelavanie/login.php"
  predmety_url = "https://vzdelavanie.uniza.sk/vzdelavanie/prihlas_pred.php"
  
  s = requests.Session()
  username = input("Enter your username: ")
  password = input("Enter your password: ")
  subjects = input("Enter comma-separated subjects: ").split(",")
  check_delay = int(input("Enter delay between checks (seconds): "))

  print("Signing in vzdelavanie.uniza.sk...")
  response = s.post(login_url, data = { "meno": username, "heslo": password })

  if response.json()["logged"]:
    print("Login successful")
  else:
    print("Login failed")
    return

  while True:
    response = s.get(predmety_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    predmet_rows = soup.find_all("tr", class_=["odd", "evn", "rgreen"])
    os.system("cls")

    for predmet_row in predmet_rows:
      predmet_cols = predmet_row.find_all("td")
      predmet_nazov = predmet_cols[0].text[7:].strip()
      predmet_miesta = predmet_cols[2].text

      if predmet_nazov in subjects:
        miesta_split = predmet_miesta.split(" / ")
        color = "\033[91m" if int(miesta_split[1]) >= int(miesta_split[0]) else "\033[92m"

        print("{}{} - {} \033[0m".format(color, predmet_nazov, predmet_miesta))
    test = test + 1
    time.sleep(check_delay)

if __name__ == "__main__":
  main()