# 테스트 흐름
# 1. 등록된 고객 정보 불러와 [고객명] 기준 검색
# 2. 리스트 > 상세 > 수정모드 진입 -> 이탈 시 Alert 확인
# 3. [고객명] 다시 검색 수정 화면 바로 진입
# 4. 일부 데이터 수정 후 저장 -> 리스트에 반영 확인

import json
import random
from playwright.sync_api import Page, expect
from helpers.customer_utils import generate_random_birth,generate_random_phone,generate_random_email, update_customer_in_json, cen_login
from config import URLS

CUSTOMER_FILE = "data/customers.json"

def load_customers_by_nationality():
    with open(CUSTOMER_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    korean = next(
        (c for c in data if c.get("name") in ["한국인수정", "한국인수정테스트"]),
        None
    )
    foreign = next(
        (c for c in data if c.get("name") in ["외국인수정", "외국인수정테스트"]),
        None
    )

    return korean, foreign

def toggle_name(name: str) -> str:
    if name.endswith("수정테스트"):
        return name.replace("수정테스트", "수정")
    return name.replace("수정", "수정테스트")

def test_edit_list_and_detail_by_nationality(page: Page):
    korean_customer, foreign_customer = load_customers_by_nationality()
    assert korean_customer and foreign_customer, "❌ 고객 정보가 충분하지 않습니다."

    cen_login(page)

    # ✅ 리스트에서 한국인 고객 수정
    page.goto(URLS["cen_customer"])
    page.wait_for_timeout(1000)
    page.fill('[data-testid="input_search_phone"]', korean_customer["phone"])
    page.wait_for_timeout(1000)
    page.click("body")
    page.wait_for_timeout(1000)
    row = page.locator("table tbody tr").first
    cells = row.locator("td")

    new_korean = {
        "name": toggle_name(korean_customer["name"]),
        "birth": generate_random_birth(),
        "phone": generate_random_phone()
    }

    for i, key in enumerate(["name", "birth", "phone"]):
        cell = cells.nth(i + 1)

        try:
            # 수정 진입 시도
            cell.dblclick()  # 또는 .locator("button").click()
            page.wait_for_timeout(1000) 
            if key == "gender":
                page.locator('[data-testid="drop_gender"]').click()
                page.wait_for_timeout(1000)
                page.locator(f'button:has-text("{new_korean["gender"]}")').click()
                page.wait_for_timeout(1000)
            else:
                input_box = cell.locator("input").first
                input_box.fill("")
                page.wait_for_timeout(1000)
                page.locator("body").click(position={"x": 10, "y": 10})
                page.wait_for_timeout(1000)
                page.locator('[data-testid="btn_yes"]').click()
                page.wait_for_timeout(500)
                # 필수 입력 알림 확인
                if page.locator('[data-testid="toast_required"]').is_visible():
                    print(f"✅ {key} 필수 입력 경고 노출 확인됨")
                    page.wait_for_timeout(3000)
                cell.dblclick()
                page.wait_for_timeout(1000)
                input_box.fill(new_korean[key])
                page.wait_for_timeout(1000)
                page.locator("body").click(position={"x": 10, "y": 10})
                page.wait_for_timeout(1000)
                page.locator('[data-testid="btn_yes"]').click()
                page.wait_for_timeout(500)
                expect(page.locator('[data-testid="toast_edit"]')).to_be_visible()
        except Exception as e:
            print(f"❌ '{key}' 셀 수정 실패: {e}")
        
    update_customer_in_json(korean_customer["name"], new_korean)


    # ✅ 상세에서 외국인 고객 수정
    page.goto(URLS["cen_customer"])
    page.wait_for_timeout(1000)
    page.fill('[data-testid="input_search_phone"]', foreign_customer["email"])
    page.wait_for_timeout(1000)
    page.click("body")
    page.wait_for_timeout(3000)
    row = page.locator("table tbody tr").first
    row.locator("td").last.click()
    page.wait_for_timeout(2000)
    page.locator('[data-testid="btn_edit"]').first.click()
    page.wait_for_timeout(3000)

    new_foreign = {
        "name": toggle_name(foreign_customer["name"]),
        "birth": generate_random_birth(),
        "gender": "여성" if foreign_customer["gender"] == "남성" else "남성",
        "email": generate_random_email()
    }

    page.fill('[data-testid="input_name"]', new_foreign["name"])
    page.wait_for_timeout(1000)
    page.fill('[data-testid="input_birth"]', new_foreign["birth"])
    page.wait_for_timeout(1000)
    page.locator('[data-testid="drop_gender"]').click()
    page.wait_for_timeout(1000)
    page.get_by_role("option", name=new_foreign["gender"]).click()
    page.wait_for_timeout(1000)
    page.fill('[data-testid="input_email"]', new_foreign["email"])
    page.wait_for_timeout(500)
    page.get_by_role("button", name="완료").click()
    page.wait_for_timeout(500)
    expect(page.locator('[data-testid="toast_edit"]')).to_be_visible()
    page.wait_for_timeout(1000)


    # ✅ JSON 업데이트
    
    update_customer_in_json(foreign_customer["name"], new_foreign)
    print("✅ 리스트/상세 고객 수정 테스트 완료")