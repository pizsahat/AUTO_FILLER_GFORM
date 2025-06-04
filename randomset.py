import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from faker import Faker

fake = Faker('id_ID')

def generate_realistic_data():
    """Generate realistic demographic and response data"""
    
    # Gender distribution
    genders = ['Laki-laki', 'Perempuan']
    gender = random.choice(genders)
    
    # Age distribution (more realistic)
    ages = ['<18', '18–25', '26–35', '>35']
    age_weights = [0.1, 0.4, 0.35, 0.15]  # More realistic age distribution
    age = random.choices(ages, weights=age_weights)[0]
    
    # Education level based on age
    if age == '<18':
        education_options = ['SMA/SMK']
        education_weights = [1.0]
    elif age == '18–25':
        education_options = ['SMA/SMK', 'D3', 'S1']
        education_weights = [0.3, 0.2, 0.5]
    elif age == '26–35':
        education_options = ['SMA/SMK', 'D3', 'S1', 'S2/S3']
        education_weights = [0.25, 0.15, 0.5, 0.1]
    else:  # >35
        education_options = ['SD', 'SMA/SMK', 'D3', 'S1', 'S2/S3']
        education_weights = [0.05, 0.3, 0.15, 0.4, 0.1]
    
    education = random.choices(education_options, weights=education_weights)[0]
    
    # Status based on age and education
    if age == '<18':
        status_options = ['Mahasiswa']
        status_weights = [1.0]
    elif age == '18–25':
        if education in ['SMA/SMK', 'D3', 'S1']:
            status_options = ['Mahasiswa', 'Pegawai/Karyawan', 'Wirausaha']
            status_weights = [0.6, 0.3, 0.1]
        else:
            status_options = ['Mahasiswa', 'Pegawai/Karyawan']
            status_weights = [0.7, 0.3]
    else:  # 26+ years
        status_options = ['Mahasiswa', 'Pegawai/Karyawan', 'Wirausaha', 'Lainnya']
        status_weights = [0.1, 0.6, 0.25, 0.05]
    
    status = random.choices(status_options, weights=status_weights)[0]
    
    # Generate ratings (1-5) with realistic distribution
    # Most responses tend to be 3-5, with some variation
    ratings = []
    for _ in range(14):  # 14 rating questions total
        rating_weights = [0.05, 0.1, 0.25, 0.35, 0.25]  # 1-5 distribution
        rating = random.choices([1, 2, 3, 4, 5], weights=rating_weights)[0]
        ratings.append(rating)
    
    return {
        'gender': gender,
        'age': age,
        'education': education,
        'status': status,
        'ratings': ratings
    }

def fill_google_form(num_responses):
    # Setup Chrome options untuk stabilitas
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Inisialisasi WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    successful_submissions = 0
    
    for attempt in range(num_responses):
        try:
            # Generate realistic data for this submission
            data = generate_realistic_data()
            
            print(f"\n=== Mengisi form ke-{attempt + 1} ===")
            print(f"Data: {data['gender']} {data['age']} {data['education']} {data['status']}")
            print(f"Ratings: {' '.join(map(str, data['ratings']))}")
            
            # Buka URL Google Form
            driver.get("YOUR_GOOGLE_FORM_URL")
            
            # Tunggu hingga form siap
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "form"))
            )
            time.sleep(2)
            
            # === HALAMAN 1 ===
            print("Mengisi Halaman 1...")
            
            # 1. Isi Nama
            name = fake.name()
            print(f"Mengisi nama: {name}")
            
            if not fill_text_field(driver, name, "Nama"):
                print("Gagal mengisi nama, skip form ini")
                continue
            
            time.sleep(1)
            
            # 2. Pilih Jenis Kelamin
            gender_index = 0 if data['gender'] == 'Laki-laki' else 1
            if not fill_radio_question(driver, "Jenis Kelamin", gender_index):
                print("Gagal memilih jenis kelamin")
                continue
            
            time.sleep(1)
            
            # 3. Pilih Usia
            age_mapping = {'<18': 0, '18–25': 1, '26–35': 2, '>35': 3}
            age_index = age_mapping[data['age']]
            if not fill_radio_question(driver, "Usia", age_index):
                print("Gagal memilih usia")
                continue
            
            time.sleep(1)
            
            # 4. Pilih Status
            status_mapping = {'Mahasiswa': 0, 'Pegawai/Karyawan': 1, 'Wirausaha': 2, 'Lainnya': 3}
            status_index = status_mapping.get(data['status'], 0)
            if not fill_radio_question(driver, "Status", status_index):
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
            
            # Isi 7 pertanyaan rating scale (1-5) di halaman 2
            page2_questions = [
                "kurikulum yang relevan",
                "metode pembelajaran",
                "kemampuan berpikir kritis", 
                "fasilitas pembelajaran",
                "evaluasi atau ujian",
                "etika dan sikap tanggung jawab",
                "bekal nyata untuk dunia kerja"
            ]
            
            for i, question_desc in enumerate(page2_questions):
                # Gunakan rating dari data yang sudah digenerate
                rating = data['ratings'][i]
                rating_index = rating - 1  # Convert to 0-based index
                if not fill_rating_question(driver, i+1, rating_index, question_desc):
                    print(f"Warning: Gagal mengisi pertanyaan {i+1}: {question_desc}")
                time.sleep(0.5)
            
            # Klik tombol "Berikutnya" untuk ke halaman 3
            if not click_next_button(driver, "Halaman 2"):
                print("Gagal klik tombol Berikutnya di halaman 2")
                continue
            
            # === HALAMAN 3 ===
            print("Mengisi Halaman 3...")
            time.sleep(2)
            
            # Isi 7 pertanyaan rating scale (1-5) di halaman 3
            page3_questions = [
                "keterampilan di lingkungan kerja",
                "mengatur waktu dan menyelesaikan tugas",
                "nilai integritas dan kejujuran",
                "beradaptasi dengan situasi baru",
                "mencari solusi kreatif",
                "percaya diri berkomunikasi",
                "semangat terus belajar"
            ]
            
            for i, question_desc in enumerate(page3_questions):
                # Gunakan rating dari data yang sudah digenerate (lanjutan dari halaman 2)
                rating = data['ratings'][i + 7]  # Start from index 7
                rating_index = rating - 1  # Convert to 0-based index
                if not fill_rating_question(driver, i+1, rating_index, question_desc):
                    print(f"Warning: Gagal mengisi pertanyaan {i+1}: {question_desc}")
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
            print(f"❌ Error pada form ke-{attempt + 1}: {e}")
            continue
    
    driver.quit()
    print(f"\n🎉 Proses selesai! Berhasil submit {successful_submissions} dari {num_responses} form.")

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
        
        # Tentukan index radio group berdasarkan tipe pertanyaan
        group_index = 0
        if question_type == "Jenis Kelamin":
            group_index = 0
        elif question_type == "Usia":
            group_index = 1
        elif question_type == "Status":
            group_index = 2
        
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
        print(f"❌ Error mengisi {question_type}: {e}")
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
        print(f"❌ Error rating question {question_number}: {e}")
        return False

def click_next_button(driver, current_page):
    """Klik tombol Berikutnya dengan berbagai selector"""
    selectors = [
        "div[role='button']:contains('Berikutnya')",
        "span:contains('Berikutnya')",
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
            if ":contains" in selector:
                continue  # Skip CSS contains selector
            
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
        "div[role='button']:contains('Kirim')",
        "span:contains('Kirim')",
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
            if ":contains" in selector:
                continue
            
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
        num_responses = int(input("Masukkan jumlah responden yang ingin dibuat: "))
        if num_responses <= 0:
            print("Jumlah responden harus lebih dari 0")
        else:
            fill_google_form(num_responses)
    except ValueError:
        print("Harap masukkan angka yang valid")
    except KeyboardInterrupt:
        print("\nProses dihentikan oleh user")
    except Exception as e:
        print(f"Error: {e}")