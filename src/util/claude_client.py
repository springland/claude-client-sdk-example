
import os
import anthropic
import json
from pathlib import Path
from util.get_windows_credential import get_windows_credential
def  load_llm_profile(llm_profile_name:str = "deepseek"):
    project_root = Path(__file__).resolve().parents[2]


    profile_path = project_root / "profiles" / f"{llm_profile_name}.json"

    with profile_path.open(encoding="utf-8") as file:
        profile = json.load(file)
        return profile

def  get_claude_client_and_default_model():
    llm_profile_name = os.getenv("LLM_PROFILE", "deepseek")
    print(f"llm profle name : {llm_profile_name}")
    profile = load_llm_profile(llm_profile_name)

    api_key = get_windows_credential(profile["credential_name"])['password']
    client = anthropic.Anthropic(
        base_url= profile["base_url"],
        api_key= api_key
    )

    return client , profile["model"]