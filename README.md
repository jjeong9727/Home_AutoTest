# 🏠 Home/Centurion_AutoTest
> 🧪 **자동화 테스트 프로젝트**  
> 사용 기술: `Python` + `Playwright`

---------------------------------

## 📁 프로젝트 디렉토리 구조

### 1. Root
- 최상단 폴더
- `config.py`  
  > 공통 변수 저장 파일 (예: URL, 계정 정보 등)
  
- `.gitignore`  
  > Git 커밋 시 대상에서 제외할 데이터를 명시하는 파일
  > 개인 정보 / URL 등 공유 불가 데이터 등 
  > `.env` 등등 
---------------------------------

### 2. `data/` 폴더
테스트에서 사용하는 **데이터 파일**들을 저장합니다.

- `language.xlsx`  
  > 다국어 매핑 정보가 저장된 엑셀 파일  
  > 유지보수를 위해 엑셀에서 관리하며, 이후 `json` 파일로 변환되어 활용됨

- `language.json`  
  > `language.xlsx`에서 생성된 다국어 매핑 JSON 데이터  
  > 실제 자동화 테스트에서 사용하는 **실제 문자열 데이터**

- `device_profile.json`  
  > 모바일 테스트 대상 단말 정보  
  > 해상도, 브라우저 종류 등 기기 설정값 포함

- `customers.json`  
  > 등록된 고객의 정보 저장 파일  
  > 이름 | 생년월일 | 성별 | 전화번호 | 이메일 | 국적 | 멤버십 등급 | 멤버십 총 금액 | 마일리지 | 멤버십 보유 금액

- `reservation.json`  
  > 등록된 예약 내역 저장 파일  
  > 예약 고객 | 생년월일 | 성별 | 전화번호 | 예약 일자 | 예약 상태 `[대기|확정|취소]`

- `daily_count.json`  
  > 날짜별 카운트 정보 저장 파일   
  > 이름 생성을 위한 날짜+넘버링 `[0101.1]` 저장


---

### 3. `helpers/` 폴더
테스트에 필요한 **공통 유틸리티 코드**를 보관합니다.  
예: 공통 함수, 필터링 로직 등

- `auth_helpers.py`  
  > home / centurion 로그인 access_token 받기 위한 파일  

- `customer_utils.py`  
  > CEN 고객설정 테스트에 사용하는 공통 함수 저장 파일
  
- `reservation_utils.py`  
  > CEN 예약설정 테스트에 사용하는 공통 함수 저장 파일

- `homepage_utils.py`  
  > HOME 테스트에 사용하는 공통 함수 저장 파일    
  
- `nav_menu.py`  
  > HOME 메뉴 `[대분류>중분류>소분류]` 진입 함수 저장 파일


---

### 4. `scripts/` 폴더
사전 준비 또는 테스트 후 후처리를 위한 **실행용 스크립트** 모음입니다.

- `language_mapping.py`  
  > `language.xlsx` → `language.json` 변환 스크립트  
  > 다국어 테스트 데이터를 자동 변환

- `delete_account.py`  
  > 홈페이지 계정 삭제 API 호출 함수
  > .env 파일에 명시한 계정 삭제 처리

---

### 5. `tests/` 폴더
실제 **자동화 테스트 케이스**들이 들어 있는 핵심 폴더입니다.

- `conftest.py`  
  > 웹 및 모바일(Android, iOS) 테스트 설정 및 브라우저 구성  
  > 모든 테스트 파일에 영향을 주는 공통 설정

- `.env`  
  > 테스트에 사용하는 보안이 필요한 데이터 저장
  > Webhook URL, API Endpoint, Account 등등 

### 5-1. `centurion`
- `test_reservation~.py`
  > 예약 설정 > 예약 관리 화면 테스트
  > 예약 추가 / 수정 / 확정 및 취소 / 검색

- `test_customer~.py`
  > 고객 설정 > 고객 관리 화면 테스트
  > 고객 등록 / 수정 / 검색

- `test_customer~.py`
  > 고객 설정 > 멤버십 등급 관리 화면 테스트
  > 고객 등급 설정 / 멤버십 충전 및 사용 

### 5-2. `home`
- `test_menu_nav.py`  
  > 홈페이지 진입 및 주요 UI 요소 노출 여부 테스트

- `test_language.py`  
  > 홈페이지 주요 요소 한국어 / 영어 번역 확인 테스트  

- `test_membership.py`  
  > 특정 고객의 고객 정보 및 멤버십 보유 금액 확인 테스트
  > customer.json 파일과 실제 서버 데이터 비교
  > 로그인 토큰 사용함에 따라 1개 계정 고정으로 테스트 
---

## 📌 기타
- 테스트 실행 시 `웹`, `Android`, `iOS` 브라우저 환경에서 **동일한 테스트가 병렬로 실행**됨
- 데이터와 테스트 파일의 구조를 분리하여 **유지보수성과 확장성** 확보
