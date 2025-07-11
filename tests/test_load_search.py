import asyncio
import pytest
import httpx
import time

URL = "http://localhost:8000/user/search"

@pytest.mark.asyncio
async def test_search_users_load():
    users = 1000
    total_requests = 100
    requests_per_user = total_requests // users

    async def user_task(user_id):
        params = {
            "firstName": "А",
            "lastName": "К"
        }
        durations = []

        async with httpx.AsyncClient(timeout=30.0) as client:
            for i in range(requests_per_user):
                start = time.perf_counter()
                response = await client.get(URL, params=params)
                duration = time.perf_counter() - start
                assert response.status_code == 200
                durations.append(duration)
        return durations

    total_start = time.perf_counter()

    # Запускаем всех пользователей параллельно
    tasks = []
    for i in range(users):
        tasks.append(user_task(i))

    results = await asyncio.gather(*tasks)

    total_duration = time.perf_counter() - total_start

    # Распаковываем времена всех запросов
    all_durations = []
    for user_durations in results:
        for d in user_durations:
            all_durations.append(d)

    # Статистика
    print(f"\n--- Результаты ---")
    print(f"Всего запросов: {total_requests}")
    print(f"Количество пользователей: {users}")
    print(f"Min latency: {min(all_durations):.4f} sec")
    print(f"Max latency: {max(all_durations):.4f} sec")
    print(f"Avg latency: {sum(all_durations)/len(all_durations):.4f} sec")
    print(f"Total time:  {total_duration:.4f} sec")
    print(f"Throughput:  {total_requests / total_duration:.2f} requests/sec")
