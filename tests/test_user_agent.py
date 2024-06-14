import requests
import pytest

user_agent_data = [
    (
        "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Mobile",
        "No",
        "Android"
    ),
    (
        "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
        "Mobile",
        "Chrome",
        "iOS"
    ),
    (
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Googlebot",
        "Unknown",
        "Unknown"
    ),
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
        "Web",
        "Chrome",
        "No"
    ),
    (
        "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "Mobile",
        "No",
        "iPhone"
    )
]

@pytest.fixture(scope="module")
def failed_user_agents():
    failed_agents = []
    yield failed_agents

    if failed_agents:
        print(f"Wrong {failed_agents}:")
        for agent in failed_agents:
            print(f"- {agent}")

@pytest.mark.parametrize("user_agent, expected_platform, expected_browser, expected_device", user_agent_data)
def test_user_agent_check(user_agent, expected_platform, expected_browser, expected_device, failed_user_agents):
    # Отправляем GET-запрос с указанным User-Agent
    response = requests.get(
        "https://playground.learnqa.ru/ajax/api/user_agent_check",
        headers={"User-Agent": user_agent}
    )

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    result = response.json()

    if result["platform"] != expected_platform or result["browser"] != expected_browser or result[
        "device"] != expected_device:
        failed_user_agents.append(user_agent)

    assert result[
               "platform"] == expected_platform, f"Platform mismatch. Expected: {expected_platform}, Got: {result['platform']}"
    assert result[
               "browser"] == expected_browser, f"Browser mismatch. Expected: {expected_browser}, Got: {result['browser']}"
    assert result["device"] == expected_device, f"Device mismatch. Expected: {expected_device}, Got: {result['device']}"

