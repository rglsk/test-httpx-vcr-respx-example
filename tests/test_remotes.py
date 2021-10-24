from typing import Any, Dict

import pytest
import respx
from httpx import Response

from remotes import FakerService

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="module")
def vcr_config() -> Dict[str, Any]:
    return {
        "filter_headers": ["authorization", "host"],
        "ignore_localhost": True,
        "record_mode": "once",
    }


@pytest.mark.respx(base_url=FakerService.base_url)
async def test_faker_service_get_using_respx(respx_mock: respx.MockRouter) -> None:

    respx_mock.get("/api/v1/books?_quantity=1").mock(
        return_value=Response(
            200,
            json={
                "title": "First, because I'm.",
                "author": "Enola Lang",
                "genre": "Iste",
            },
        )
    )

    response = await FakerService.get("/api/v1/books?_quantity=1")
    assert response == {
        "title": "First, because I'm.",
        "author": "Enola Lang",
        "genre": "Iste",
    }


@pytest.mark.vcr()
async def test_faker_service_get() -> None:
    response = await FakerService.get(
        "/api/v1/books?_quantity=1", params={"param1": "qwerty"}
    )

    assert response == {
        "status": "OK",
        "code": 200,
        "total": 1,
        "data": [
            {
                "status": "OK",
                "code": 200,
                "total": 1,
                "data": [
                    {
                        "title": "Cat. 'Do you play.",
                        "author": "Mervin Zulauf",
                        "genre": "Ad",
                        "description": (
                            "I've got to the porpoise, \"Keep back, please: we don't want to be?'"
                            "it asked. 'Oh, I'm not myself, you see.' 'I don't quite understand you,'"
                            " she said, without opening its eyes, 'Of course, of."
                        ),
                        "isbn": "9782943949905",
                        "image": "http://placeimg.com/480/640/any",
                        "published": "1998-09-03",
                        "publisher": "Ut Sapiente",
                    }
                ],
            }
        ],
    }


@pytest.mark.vcr()
async def test_faker_service_multiple_gets() -> None:
    responses = [await FakerService.get("/api/v1/books?_quantity=1") for _ in range(2)]

    assert responses[0] == {
        "status": "OK",
        "code": 200,
        "total": 1,
        "data": [
            {
                "title": "Alice began.",
                "author": "Carmella Osinski",
                "genre": "Labore",
                "description": (
                    "I didn't!' interrupted Alice. 'You are,' said the Mock Turtle, 'they--you've seen them, "
                    "of course?' 'Yes,' said Alice to herself, 'because of his pocket, and pulled out a "
                    "history of the month, and."
                ),
                "isbn": "9797084459572",
                "image": "http://placeimg.com/480/640/any",
                "published": "1978-08-10",
                "publisher": "Quos Ullam",
            }
        ],
    }
    assert responses[1] == {
        "status": "OK",
        "code": 200,
        "total": 1,
        "data": [
            {
                "title": "Queen, the royal.",
                "author": "Jayce Pacocha",
                "genre": "Earum",
                "description": (
                    "They all sat down at once, she found herself in the night? Let me think: was I the "
                    "same as the rest of the crowd below, and there stood the Queen merely remarking "
                    "as it spoke. 'As wet as ever,' said."
                ),
                "isbn": "9784458758737",
                "image": "http://placeimg.com/480/640/any",
                "published": "2002-07-04",
                "publisher": "Aspernatur Quis",
            }
        ],
    }
