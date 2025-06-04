import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options

# Sample data structure (FIXED: removed education field from index 2)
sample_data = [
    ["Perempuan", "<18", "Mahasiswa", 4, 4, 5, 2, 4, 1, 3, 4, 2, 3, 4, 4, 3, 4],
    ["Perempuan", "<18", "Pegawai/Karyawan", 3, 3, 5, 3, 2, 2, 5, 4, 5, 5, 4, 5, 4, 4],
    ["Perempuan", "26–35", "Pegawai/Karyawan", 4, 1, 3, 3, 2, 3, 2, 3, 4, 4, 4, 3, 3, 5],
    ["Perempuan", "26–35", "Pegawai/Karyawan", 3, 4, 5, 4, 4, 4, 5, 5, 3, 2, 4, 3, 3, 5],
    ["Perempuan", "18–25", "Mahasiswa", 5, 4, 3, 3, 4, 3, 4, 5, 4, 3, 5, 4, 2, 2],
    ["Laki-laki", "26–35", "Pegawai/Karyawan", 2, 4, 5, 4, 5, 5, 1, 5, 4, 4, 3, 4, 3, 4],
    ["Laki-laki", ">35", "Mahasiswa", 4, 3, 5, 5, 3, 4, 4, 3, 5, 4, 5, 4, 1, 4],
    ["Laki-laki", ">35", "Wirausaha", 3, 2, 5, 5, 2, 4, 2, 5, 5, 3, 4, 4, 3, 5],
    ["Laki-laki", "18–25", "Pegawai/Karyawan", 3, 3, 5, 4, 4, 4, 2, 3, 4, 4, 3, 3, 2, 4],
    ["Laki-laki", ">35", "Mahasiswa", 3, 4, 3, 2, 5, 4, 4, 5, 5, 3, 2, 4, 4, 4],
    ["Perempuan", "26–35", "Mahasiswa", 4, 3, 5, 3, 3, 4, 4, 3, 3, 5, 4, 5, 4, 2],
    ["Perempuan", ">35", "Wirausaha", 5, 3, 4, 3, 4, 2, 4, 5, 3, 5, 4, 4, 5, 5],
    ["Perempuan", "26–35", "Mahasiswa", 5, 4, 4, 4, 2, 4, 4, 5, 3, 5, 2, 3, 4, 4],
    ["Laki-laki", "18–25", "Mahasiswa", 4, 4, 4, 4, 4, 5, 3, 5, 3, 4, 4, 3, 4, 5],
    ["Laki-laki", "26–35", "Lainnya", 2, 3, 3, 5, 5, 5, 4, 3, 5, 5, 4, 5, 4, 1],
    ["Perempuan", "18–25", "Wirausaha", 2, 2, 2, 4, 3, 4, 4, 3, 4, 3, 4, 5, 5, 2],
    ["Laki-laki", "18–25", "Pegawai/Karyawan", 4, 3, 4, 4, 4, 1, 2, 5, 5, 4, 5, 4, 3, 3],
    ["Laki-laki", ">35", "Wirausaha", 5, 3, 3, 2, 5, 5, 4, 4, 3, 5, 5, 5, 5, 5],
    ["Laki-laki", "26–35", "Wirausaha", 5, 5, 5, 3, 5, 2, 5, 5, 3, 5, 4, 4, 5, 3],
    ["Laki-laki", "18–25", "Wirausaha", 5, 3, 4, 4, 5, 4, 5, 3, 5, 3, 5, 3, 3, 4],
    ["Perempuan", "18–25", "Pegawai/Karyawan", 4, 4, 3, 4, 1, 5, 4, 5, 5, 4, 4, 2, 4, 4],
    ["Laki-laki", ">35", "Mahasiswa", 3, 4, 4, 3, 2, 4, 5, 4, 5, 4, 4, 4, 1, 3],
    ["Laki-laki", "26–35", "Pegawai/Karyawan", 4, 3, 4, 5, 5, 3, 2, 4, 4, 4, 5, 5, 4, 3],
    ["Laki-laki", "<18", "Pegawai/Karyawan", 5, 2, 4, 4, 3, 4, 4, 3, 4, 1, 5, 5, 3, 4],
    ["Laki-laki", ">35", "Mahasiswa", 3, 5, 4, 5, 4, 5, 4, 5, 5, 4, 5, 4, 5, 4],
    ["Perempuan", "26–35", "Mahasiswa", 3, 4, 5, 4, 4, 3, 2, 3, 3, 4, 4, 3, 3, 4],
    ["Perempuan", "18–25", "Pegawai/Karyawan", 4, 3, 4, 5, 4, 4, 5, 5, 4, 1, 4, 5, 5, 5],
    ["Laki-laki", "26–35", "Pegawai/Karyawan", 3, 3, 4, 1, 3, 4, 4, 3, 4, 3, 4, 2, 4, 4],
    ["Laki-laki", "26–35", "Pegawai/Karyawan", 2, 4, 3, 3, 5, 4, 5, 5, 3, 2, 1, 4, 5, 4],
    ["Perempuan", "26–35", "Pegawai/Karyawan", 5, 3, 1, 3, 2, 4, 4, 3, 4, 5, 3, 4, 5, 3],
    ["Perempuan", ">35", "Mahasiswa", 3, 4, 5, 4, 4, 2, 4, 4, 3, 5, 5, 4, 3, 5],
    ["Perempuan", "18–25", "Mahasiswa", 4, 3, 5, 5, 2, 5, 4, 5, 5, 4, 5, 5, 3, 5],
    ["Perempuan", "26–35", "Pegawai/Karyawan", 3, 5, 5, 2, 5, 3, 4, 4, 4, 2, 5, 3, 3, 5],
    ["Laki-laki", ">35", "Mahasiswa", 1, 5, 2, 4, 4, 5, 4, 4, 4, 5, 2, 3, 4, 4],
    ["Perempuan", "26–35", "Pegawai/Karyawan", 4, 3, 4, 3, 3, 2, 3, 3, 4, 5, 3, 3, 4, 5],
    ["Perempuan", "26–35", "Mahasiswa", 3, 3, 3, 1, 4, 3, 5, 4, 4, 3, 5, 4, 5, 4],
    ["Laki-laki", "18–25", "Mahasiswa", 5, 4, 5, 4, 2, 4, 2, 3, 4, 4, 5, 3, 5, 4],
    ["Perempuan", "18–25", "Pegawai/Karyawan", 4, 5, 5, 3, 4, 4, 4, 5, 3, 3, 4, 3, 3, 2],
    ["Laki-laki", "26–35", "Mahasiswa", 3, 4, 4, 4, 4, 5, 5, 4, 4, 5, 4, 4, 4, 5],
    ["Perempuan", "18–25", "Mahasiswa", 4, 4, 3, 2, 4, 4, 5, 4, 4, 2, 2, 4, 4, 3],
    ["Laki-laki", ">35", "Pegawai/Karyawan", 5, 5, 4, 3, 1, 5, 4, 4, 5, 3, 4, 4, 4, 2],
    ["Laki-laki", "18–25", "Wirausaha", 3, 4, 3, 5, 5, 4, 4, 4, 4, 5, 4, 4, 5, 4],
    ["Perempuan", "18–25", "Mahasiswa", 5, 4, 5, 3, 4, 5, 4, 4, 3, 5, 4, 3, 3, 4],
    ["Perempuan", "18–25", "Wirausaha", 4, 2, 5, 4, 4, 4, 3, 5, 5, 3, 4, 4, 5, 4],
    ["Perempuan", ">35", "Pegawai/Karyawan", 4, 5, 4, 5, 3, 3, 4, 5, 4, 3, 4, 4, 4, 4]
]

def fill_google_form(num_responses):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    successful_submissions = 0
    
    for attempt in range(min(num_responses, len(sample_data))):
        try:
            data = sample_data[attempt]
            print(f"\n=== Mengisi form ke-{attempt + 1} ===")
            print(f"Data yang digunakan: {data}")
            
            # Buka URL Google Form
            driver.get("YOUR_GOOGLE_FORM_URL")
            
            # Tunggu hingga form siap
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "form"))
            )
            time.sleep(2)
            
            # === HALAMAN 1 ===
            print("Mengisi Halaman 1...")
            
            # 1. Isi Nama (FIXED: generate name based on correct gender)
            gender = data[0]
            name = generate_name(gender)
            print(f"Mengisi nama: {name} (Gender: {gender})")
            
            if not fill_text_field(driver, name, "Nama"):
                print("Gagal mengisi nama, skip form ini")
                continue
            
            time.sleep(1)
            
            # 2. Pilih Jenis Kelamin
            gender_choice = 0 if data[0] == "Perempuan" else 1
            if not fill_radio_question(driver, "Jenis Kelamin", gender_choice):
                print("Gagal memilih jenis kelamin")
                continue
            
            time.sleep(1)
            
            # 3. Pilih Usia
            age_mapping = {"<18": 0, "18–25": 1, "26–35": 2, ">35": 3}
            age_choice = age_mapping.get(data[1], 1)  # Default to 18-25 if not found
            if not fill_radio_question(driver, "Usia", age_choice):
                print("Gagal memilih usia")
                continue
            
            time.sleep(1)
            
            # 4. Pilih Status (FIXED: now using index 2 instead of 3)
            status_mapping = {
                "Mahasiswa": 0, 
                "Pegawai/Karyawan": 1, 
                "Wirausaha": 2,
                "Lainnya": 3
            }
            status_choice = status_mapping.get(data[2], 0)  # Default to Mahasiswa
            if not fill_radio_question(driver, "Status", status_choice):
                print("Gagal memilih status")
                continue
            
            time.sleep(1)
            
            # Klik tombol "Berikutnya" untuk ke halaman 2
            if not click_next_button(driver, "Halaman 1"):
                print("Gagal klik tombol Berikutnya di halaman 1")
                continue
            
            # === HALAMAN 2 ===
            print("Mengisi Halaman 2...")
            time.sleep(2)
            
            # Isi 7 pertanyaan rating scale (1-5) di halaman 2 (FIXED: now using index 3-9)
            page2_ratings = data[3:10]  # Ratings for page 2 questions
            
            for i, rating in enumerate(page2_ratings):
                # Convert rating (1-5) to index (0-4)
                rating_index = rating - 1
                if not fill_rating_question(driver, i+1, rating_index, f"Pertanyaan {i+1}"):
                    print(f"Warning: Gagal mengisi pertanyaan {i+1}")
                time.sleep(0.5)
            
            # Klik tombol "Berikutnya" untuk ke halaman 3
            if not click_next_button(driver, "Halaman 2"):
                print("Gagal klik tombol Berikutnya di halaman 2")
                continue
            
            # === HALAMAN 3 ===
            print("Mengisi Halaman 3...")
            time.sleep(2)
            
            # Isi 7 pertanyaan rating scale (1-5) di halaman 3 (FIXED: now using index 10-16)
            page3_ratings = data[10:17]  # Ratings for page 3 questions
            
            for i, rating in enumerate(page3_ratings):
                # Convert rating (1-5) to index (0-4)
                rating_index = rating - 1
                if not fill_rating_question(driver, i+1, rating_index, f"Pertanyaan {i+1}"):
                    print(f"Warning: Gagal mengisi pertanyaan {i+1}")
                time.sleep(0.5)
            
            # Submit form di halaman terakhir
            if not submit_form(driver):
                print("Gagal submit form")
                continue
            
            # Tunggu konfirmasi submit
            try:
                WebDriverWait(driver, 10).until(
                    lambda driver: "formResponse" in driver.current_url or 
                                 driver.find_elements(By.CSS_SELECTOR, "div.vHW8K") or
                                 "Tanggapan Anda telah direkam" in driver.page_source or
                                 "terkirim" in driver.page_source.lower()
                )
                print(f"✅ Form ke-{attempt + 1} berhasil disubmit!")
                successful_submissions += 1
                time.sleep(3)
                
            except TimeoutException:
                print(f"❌ Timeout menunggu konfirmasi untuk form ke-{attempt + 1}")
                continue
                
        except Exception as e:
            print(f"❌ Error pada form ke-{attempt + 1}: {str(e)}")
            continue
    
    driver.quit()
    print(f"\n🎉 Proses selesai! Berhasil submit {successful_submissions} dari {num_responses} form.")

def generate_name(gender):
    """Generate Indonesian name based on gender - FIXED logic"""
    first_names_male = ["Ahmad", "Budi", "Cahya", "Dedi", "Eko", "Fajar", "Guntur", "Hadi", "Irfan", "Joko", 
                       "Kurnia", "Lutfi", "Maman", "Nanda", "Oscar", "Pandu", "Qomar", "Reza", "Sandi", "Toni"]
    first_names_female = ["Ani", "Bunga", "Citra", "Dewi", "Eka", "Fitri", "Gita", "Hani", "Intan", "Juli",
                         "Kartika", "Lila", "Maya", "Nita", "Olivia", "Putri", "Qonita", "Rani", "Sari", "Tina"]
    last_names = ["Santoso", "Prasetyo", "Wibowo", "Hidayat", "Kurniawan", "Siregar", "Halim", "Nugroho", 
                 "Susanto", "Rahardjo", "Setiawan", "Wijaya", "Gunawan", "Sari", "Putri", "Safitri"]
    
    # FIXED: Proper gender matching
    if gender == "Perempuan":
        first_name = random.choice(first_names_female)
    elif gender == "Laki-laki":
        first_name = random.choice(first_names_male)
    else:
        # Fallback for any unexpected gender value
        first_name = random.choice(first_names_male + first_names_female)
    
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"

def fill_text_field(driver, text, field_name):
    """Mengisi field text dengan berbagai selector"""
    selectors = [
        "input[type='text']",
        "input[aria-labelledby*='i1']",
        "div[data-params*='textQuestion'] input",
        "input.quantumWizTextinputPaperinputInput",
        ".Xb9hP input"
    ]
    
    for selector in selectors:
        try:
            field = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            field.clear()
            field.send_keys(text)
            print(f"✅ {field_name} berhasil diisi: {text}")
            return True
        except:
            continue
    
    print(f"❌ Gagal mengisi {field_name}")
    return False

def fill_radio_question(driver, question_type, choice_index):
    """Mengisi pertanyaan radio button berdasarkan index pilihan"""
    try:
        # Tunggu sampai radio groups tersedia
        radio_groups = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='radiogroup']"))
        )
        
        # Tentukan index radio group berdasarkan tipe pertanyaan (FIXED: adjusted indexes)
        group_index = {
            "Jenis Kelamin": 0,
            "Usia": 1,
            "Status": 2  # FIXED: Status is now at index 2 (no more Pendidikan field)
        }.get(question_type, 0)
        
        if group_index < len(radio_groups):
            options = radio_groups[group_index].find_elements(By.CSS_SELECTOR, "div[role='radio']")
            
            if choice_index < len(options):
                # Scroll ke elemen
                driver.execute_script("arguments[0].scrollIntoView(true);", options[choice_index])
                time.sleep(0.5)
                
                # Klik pilihan
                driver.execute_script("arguments[0].click();", options[choice_index])
                print(f"✅ {question_type} berhasil dipilih (pilihan {choice_index + 1})")
                return True
        
        print(f"❌ Gagal memilih {question_type}")
        return False
        
    except Exception as e:
        print(f"❌ Error mengisi {question_type}: {str(e)}")
        return False

def fill_rating_question(driver, question_number, rating_index, description):
    """Mengisi pertanyaan rating scale (1-5)"""
    try:
        # Cari semua radio groups di halaman saat ini
        radio_groups = driver.find_elements(By.CSS_SELECTOR, "div[role='radiogroup']")
        
        if question_number - 1 < len(radio_groups):
            group = radio_groups[question_number - 1]
            options = group.find_elements(By.CSS_SELECTOR, "div[role='radio']")
            
            if rating_index < len(options):
                # Scroll ke elemen
                driver.execute_script("arguments[0].scrollIntoView(true);", options[rating_index])
                time.sleep(0.3)
                
                # Klik rating
                driver.execute_script("arguments[0].click();", options[rating_index])
                print(f"✅ Pertanyaan {question_number} ({description}): Rating {rating_index + 1}")
                return True
        
        print(f"❌ Gagal mengisi pertanyaan {question_number}")
        return False
        
    except Exception as e:
        print(f"❌ Error rating question {question_number}: {str(e)}")
        return False

def click_next_button(driver, current_page):
    """Klik tombol Berikutnya dengan berbagai selector"""
    selectors = [
        "div[role='button'] span:contains('Berikutnya')",
        "div[jsname='OCpkoe']",  # Tombol navigasi Google Form
        "div.lRwqcd div[role='button']",
        "div[aria-label*='Berikutnya']",
        ".uArJ5e.UQuaGc.Y5sE8d.ksKsZd.QvWxOd"
    ]
    
    # Coba dengan XPath untuk text content
    xpath_selectors = [
        "//span[contains(text(), 'Berikutnya')]/parent::div[@role='button']",
        "//div[@role='button' and contains(., 'Berikutnya')]",
        "//span[text()='Berikutnya']/ancestor::div[@role='button']"
    ]
    
    # Scroll ke bawah dulu untuk memastikan tombol terlihat
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    
    # Coba selector CSS
    for selector in selectors:
        try:
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            driver.execute_script("arguments[0].click();", button)
            print(f"✅ Tombol Berikutnya berhasil diklik di {current_page}")
            return True
        except:
            continue
    
    # Coba selector XPath
    for xpath in xpath_selectors:
        try:
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            driver.execute_script("arguments[0].click();", button)
            print(f"✅ Tombol Berikutnya berhasil diklik di {current_page}")
            return True
        except:
            continue
    
    print(f"❌ Gagal menemukan tombol Berikutnya di {current_page}")
    return False

def submit_form(driver):
    """Submit form di halaman terakhir"""
    selectors = [
        "div[role='button'] span:contains('Kirim')",
        "div[jsname='M2UYVd']",  # Submit button Google Form
        "div.lRwqcd div[role='button']",
        ".uArJ5e.UQuaGc.Y5sE8d.VkkpIf.QvWxOd"
    ]
    
    xpath_selectors = [
        "//span[contains(text(), 'Kirim')]/parent::div[@role='button']",
        "//div[@role='button' and contains(., 'Kirim')]",
        "//span[text()='Kirim']/ancestor::div[@role='button']"
    ]
    
    # Scroll ke bawah
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    
    # Coba selector CSS
    for selector in selectors:
        try:
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            driver.execute_script("arguments[0].click();", button)
            print("✅ Form berhasil disubmit")
            return True
        except:
            continue
    
    # Coba selector XPath
    for xpath in xpath_selectors:
        try:
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            driver.execute_script("arguments[0].click();", button)
            print("✅ Form berhasil disubmit")
            return True
        except:
            continue
    
    print("❌ Gagal menemukan tombol Kirim")
    return False

if __name__ == "__main__":
    try:
        num_responses = int(input("Masukkan jumlah responden yang ingin dibuat (maksimal {}): ".format(len(sample_data))))
        if num_responses <= 0:
            print("Jumlah responden harus lebih dari 0")
        elif num_responses > len(sample_data):
            print(f"Jumlah responden melebihi data sampel yang tersedia ({len(sample_data)})")
        else:
            fill_google_form(num_responses)
    except ValueError:
        print("Harap masukkan angka yang valid")
    except KeyboardInterrupt:
        print("\nProses dihentikan oleh user")
    except Exception as e:
        print(f"Error: {str(e)}")