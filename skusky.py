from bs4 import BeautifulSoup
import requests, os, time

def main():
  login_url = "https://vzdelavanie.uniza.sk/vzdelavanie/login.php"
  terms_url = "https://vzdelavanie.uniza.sk/vzdelavanie/terminy_s.php?pid="
  
  s = requests.Session()
  username = input("Enter your username: ")
  password = input("Enter your password: ")
  pid = input("Enter term PID from URL: ")
  check_delay = int(input("Enter delay between checks (seconds): "))

  print("Signing in vzdelavanie.uniza.sk...")
  response = s.post(login_url, data = { "meno": username, "heslo": password })

  if response.json()["logged"]:
    print("Login successful")
  else:
    print("Login failed")
    return

  while True:
    os.system("cls")
    response = s.get(terms_url + pid)
    soup = BeautifulSoup(response.content, 'html.parser')

    subject = soup.find("div", class_="SRH-inp2").b.text
    term_rows = soup.find("table", class_="SRH-inp2")

    print("Checking subject: " + subject)
    for term in term_rows.find_all("tr")[1:]:
      term_cols = term.find_all("td")
      if term_cols[5].text == "cvičenie":
        continue

      datetime = term_cols[0].text
      capacity = int(term_cols[3].text)
      occupied = int(term_cols[4].text)
      text_color = "\033[91m" if occupied >= capacity else "\033[92m"
      print("{}Date - {} <=> ".format(text_color, datetime), end = "")
      print("Capacity - {}/{}\033[0m".format(occupied, capacity))

    time.sleep(check_delay)

if __name__ == "__main__":
  main()