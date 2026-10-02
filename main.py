import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.requests import Request
import httpx
import requests

app = FastAPI()

# Facebook OAuth Config
FACEBOOK_CLIENT_ID = os.getenv("FACEBOOK_CLIENT_ID", "")
FACEBOOK_CLIENT_SECRET = os.getenv("FACEBOOK_CLIENT_SECRET", "")
FACEBOOK_REDIRECT_URI = os.getenv("FACEBOOK_REDIRECT_URI", "http://localhost:3000/facebook/callback")

CLIENT_ID = FACEBOOK_CLIENT_ID
CLIENT_SECRET = FACEBOOK_CLIENT_SECRET
REDIRECT_URI = FACEBOOK_REDIRECT_URI


@app.get("/facebook/login")
async def facebook_login():
    auth_url = (
        f"https://www.facebook.com/v21.0/dialog/oauth?"
        f"client_id={FACEBOOK_CLIENT_ID}&redirect_uri={FACEBOOK_REDIRECT_URI}&state={'{st=state123abc,ds=123456789}'}"
    )
    print(auth_url)
    return RedirectResponse(url=auth_url)


@app.get("/facebook/callback")
async def facebook_callback(request: Request):
    code = request.query_params.get("code")
    print("Code_", code)

    # if not code:
    #     raise HTTPException(status_code=400, detail="Authorization code not found")

    # token_response = await exchange_code_for_token(code)
    # print(token_response)
    # access_token = token_response.get("access_token")

    # print("AccessToken_", access_token)
    # if not access_token:
    #     raise HTTPException(status_code=400, detail="Access token not found")

    # user_info = await get_user_info(access_token)
    # return {"user_info": user_info}


async def exchange_code_for_token(code: str):
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=payload)
        print("ExchangeChangeResponse_", response)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()


async def get_user_info(access_token: str):
    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(user_info_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()


# Google / Airbyte Config from environment variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "https://127.0.0.1:3000/google/callback")

AIRBYTE_CLIENT_ID = os.getenv("AIRBYTE_CLIENT_ID", "")
AIRBYTE_CLIENT_SECRET = os.getenv("AIRBYTE_CLIENT_SECRET", "")
AIRBYTE_BASE_URL = os.getenv("AIRBYTE_BASE_URL", "https://api.airbyte.com/v1/")


# async def generate_airbyte_token(client_id, client_secret):
#     headers = {
#         "accept": "application/json",
#         "content-type": "application/json",
#     }
#     url = f"{AIRBYTE_BASE_URL}/applications/token"
#     response = requests.post(
#         url=url,
#         headers=headers,
#         json={
#             "client_id": client_id,
#             "client_secret": client_secret,
#         },
#     )
#     access_token = response.json()["access_token"]
#     return access_token


# @app.get("/google/login")
# async def google_login():
#     authHeader = f"Bearer {await generate_airbyte_token(AIRBYTE_CLIENT_ID, AIRBYTE_CLIENT_SECRET)}"
#     payload = {
#         "sourceType": "google-analytics-data-api",
#         "workspaceId": "b31bf4e8-de85-407e-b31a-6e6ad72a8f7b",
#         "redirectUrl": GOOGLE_REDIRECT_URI,
#     }
#     headers = {
#         "accept": "application/json",
#         "content-type": "application/json",
#         "authorization": authHeader,
#     }
#     response = requests.post(
#         "https://api.airbyte.com/v1/sources/initiateOAuth",
#         json=payload,
#         headers=headers,
#     )
#     consentUrl = response.json()["consentUrl"]
#     return RedirectResponse(url=consentUrl)


# @app.get("/google/callback")
# async def google_callback(request: Request):
#     code = request.query_params.get("code")
#     print("Code", code)
#     if not code:
#         raise HTTPException(status_code=400, detail="Authorization code not found")
#     token_response = await exchange_code_for_token(code)
#     print("Token response", token_response)
#     access_token = token_response.get("access_token")
#     if not access_token:
#         raise HTTPException(status_code=400, detail="Access token not found")
#     google_ads_accounts = await get_google_ads_accounts(access_token)
#     return {"google_ads_accounts": google_ads_accounts}


# async def get_google_ads_accounts(access_token: str):
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json",
#         "developer-token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN", ""),
#     }
#     url = "https://googleads.googleapis.com/v17/customers:listAccessibleCustomers"
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(url, headers=headers)
#             print(response.json())
#             response.raise_for_status()
#             return response.json()
#         except Exception as e:
#             print(e)


# @app.get("/request-access/{customer_id}")
# async def request_access(customer_id: str):
#     return {
#         "message": f"Requesting access to Google Ads account with customer ID: {customer_id}"
#     }
