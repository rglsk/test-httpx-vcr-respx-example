from typing import Dict, Optional, Any

import httpx


class FakerService:
    base_url: str = "https://fakerapi.it"

    @classmethod
    async def request(
        cls,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        **kwargs: Any,
    ) -> Dict[str, Any]:

        url = f"{cls.base_url}{endpoint}"
        async with httpx.AsyncClient(headers=headers) as client:
            response = await client.request(
                method=method, url=url, timeout=timeout, **kwargs
            )

        response.raise_for_status()
        return response.json()

    @classmethod
    async def get(
        cls, endpoint: str, headers: Optional[Dict[str, str]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        return await cls.request("get", endpoint, headers, **kwargs)
