import hashlib
import json
import random
import re
import time
import requests

# ================= KONFIGURASI =================
# URL Endpoint dari tab Network
URL_GET_CHALLENGE = "https://accounts.icarus.tools/connect/gfxcafe.oku.account.v2.AltchaService/GetChallenge"
URL_REQUEST_MAGIC_LINK = "https://accounts.icarus.tools/connect/gfxcafe.oku.account.v2.WaitlistService/RequestMagicLink"
# ===============================================


def get_random_ua():
  """Mengambil User-Agent acak dari file user-agent.txt"""
  try:
    with open("user-agent.txt", "r") as file:
      uas = file.read().splitlines()
      return random.choice(uas) if uas else "Mozilla/5.0"
  except FileNotFoundError:
    return (
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like"
        " Gecko) Chrome/127.0.0.0 Mobile Safari/537.36"
    )


def get_temp_email():
  """Membuat email temporer dengan sistem retry jika gagal"""
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  }

  for attempt in range(3):
    try:
      dom_res = requests.get(
          "https://api.mail.tm/domains", headers=headers, timeout=10
      )
      if dom_res.status_code != 200:
        continue
      domains = dom_res.json().get("hydra:member", [])
      if not domains:
        continue
      domain = domains[0]["domain"]

      username = "user_" + "".join(
          random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8)
      )
      email = f"{username}@{domain}"
      password = "Password123!"

      acc_payload = {"address": email, "password": password}
      acc_res = requests.post(
          "https://api.mail.tm/accounts", headers=headers, json=acc_payload, timeout=10
      )

      if acc_res.status_code == 201:
        token_res = requests.post(
            "https://api.mail.tm/token", headers=headers, json=acc_payload, timeout=10
        )
        if token_res.status_code == 200:
          token = token_res.json().get("token")
          return email, token
    except Exception:
      pass
    time.sleep(2)

  return None, None


def solve_altcha(salt, expected_challenge, max_iterations=1000000):
  """Memecahkan algoritma PoW ALTCHA"""
  print(f"[*] Memecahkan PoW (Salt: {salt[:10]}... )")
  for number in range(max_iterations):
    text_to_hash = f"{salt}{number}".encode("utf-8")
    hash_result = hashlib.sha256(text_to_hash).hexdigest()
    if hash_result == expected_challenge:
      print(f"[+] PoW Solved! Angka: {number}")
      return str(number)
  return None


def submit_registration(email, ref_code, ua):
  """Alur meminta challenge dengan menangkap struktur JSON nested"""
  headers = {
      "accept": "*/*",
      "accept-language": "id-ID",
      "connect-protocol-version": "1",
      "content-type": "application/json",
      "origin": "https://oku.trade",
      "referer": "https://oku.trade/",
      "sec-ch-ua": '"Chromium";v="127", "Not)A;Brand";v="99", "Lemur";v="127"',
      "sec-ch-ua-mobile": "?1",
      "sec-ch-ua-platform": '"Android"',
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "cross-site",
      "user-agent": ua,
  }

  challenge_payload = {
      "endpoint": (
          "/gfxcafe.oku.account.v2.WaitlistService/RequestMagicLink"
      ),
      "clientInfo": {"userAgent": ua},
      "email": email,
  }

  print("[*] Meminta Challenge dari server...")
  try:
    challenge_req = requests.post(
        URL_GET_CHALLENGE, headers=headers, json=challenge_payload, timeout=10
    )

    if challenge_req.status_code != 200 or not challenge_req.text.strip():
      print(f"[-] Server challenge error. Status: {challenge_req.status_code}")
      return False

    res_json = challenge_req.json()
    challenge_data = res_json.get("challenge", {})

    salt = challenge_data.get("salt")
    expected_challenge = challenge_data.get("challenge")
    signature = challenge_data.get("signature")
    algorithm = challenge_data.get("algorithm", "SHA-256")

    if not salt or not expected_challenge:
      print("[-] Data challenge tidak lengkap dari server.")
      return False

  except Exception as e:
    print(f"[-] Gagal mengambil challenge: {e}")
    return False

  number = solve_altcha(salt, expected_challenge)
  if not number:
    print("[-] Gagal memecahkan challenge.")
    return False

  payload = {
      "email": email,
      "referralCode": ref_code,  # Menggunakan parameter input manual
      "altchaSolution": {
          "algorithm": algorithm,
          "challenge": expected_challenge,
          "number": number,
          "salt": salt,
          "signature": signature,
      },
  }

  print(f"[*] Mengirim pendaftaran untuk: {email}")
  try:
    response = requests.post(
        URL_REQUEST_MAGIC_LINK, json=payload, headers=headers, timeout=10
    )
    if response.status_code == 200:
      print("[+] Berhasil submit form!")
      return True
    else:
      print(
          f"[-] Gagal submit. Code: {response.status_code},"
          f" Res: {response.text[:200]}"
      )
      return False
  except Exception as e:
    print(f"[-] Error request: {e}")
    return False


def verify_email(token, ua):
  """Mengecek inbox Mail.tm, mencari link verifikasi berparameter waitlistToken"""
  print("[*] Menunggu email masuk (Maks 60 detik)...")
  headers_mail = {"Authorization": f"Bearer {token}", "User-Agent": ua}

  for _ in range(12):
    time.sleep(5)
    try:
      res = requests.get(
          "https://api.mail.tm/messages", headers=headers_mail, timeout=10
      )
      if res.status_code == 200:
        messages = res.json().get("hydra:member", [])
        if len(messages) > 0:
          msg_id = messages[0]["id"]

          msg_res = requests.get(
              f"https://api.mail.tm/messages/{msg_id}",
              headers=headers_mail,
              timeout=10,
          )
          if msg_res.status_code == 200:
            msg_data = msg_res.json()
            body_text = msg_data.get("text", "")
            body_html = msg_data.get("html", "")
            if isinstance(body_html, list):
              body_html = "".join(body_html)

            full_content = str(body_text) + " " + str(body_html)
            urls = re.findall(r"(https?://[^\s\"<>]+)", full_content)

            verify_link = None
            for url in urls:
              url_lower = url.lower()
              if "waitlisttoken" in url_lower or "oku.trade/mobile" in url_lower:
                verify_link = url
                break

            if verify_link:
              verify_link = verify_link.rstrip('.)"}>\']')
              print(f"[*] Menemukan link konfirmasi: {verify_link}")
              print(f"[*] Mengeksekusi verifikasi...")

              conf_res = requests.get(
                  verify_link, headers={"User-Agent": ua}, timeout=10
              )
              print(
                  f"[+] Status Respons Verifikasi: {conf_res.status_code}"
              )
              print("[+] Verifikasi Berhasil!\n")
              return True
    except Exception as e:
      pass

  print("[-] Timeout: Email konfirmasi tidak masuk.\n")
  return False


if __name__ == "__main__":
  # Meminta input kode referral secara manual
  input_ref_code = input(
      "[?] Masukkan Kode Referral (Ref Code): "
  ).strip()
  if not input_ref_code:
    print("[-] Kode referral tidak boleh kosong!")
    exit(1)

  try:
    total_ref = int(input("[?] Mau buat berapa referral? "))
  except ValueError:
    print("[-] Masukkan angka yang valid!")
    exit(1)

  for i in range(1, total_ref + 1):
    print(f"\n========================================")
    print(f" PROSES AKUN REFERRAL KE-{i} DARI {total_ref}")
    print(f"========================================")

    ua = get_random_ua()

    # Ambil email dengan sistem retry otomatis
    email_addr, mail_token = get_temp_email()
    if not email_addr:
      print(
          "[-] Gagal total membuat email temporer setelah 3x percobaan,"
          " melewati..."
      )
      continue

    print(f"[+] Email Target: {email_addr}")

    if submit_registration(email_addr, input_ref_code, ua):
      verify_email(mail_token, ua)

    if i < total_ref:
      print("[*] Menunggu 1 detik sebelum lanjut ke akun berikutnya...")
      time.sleep(1)

  print("\n[+] Semua proses pembuatan referral selesai!")
