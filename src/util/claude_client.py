
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

def  get_claude_client_and_default_model(profile_name =None , model_name= None , api_key= None ):
    llm_profile_name = profile_name if profile_name else os.getenv("LLM_PROFILE", "deepseek")

    profile = load_llm_profile(llm_profile_name)

    api_key = api_key if api_key else get_windows_credential(profile["credential_name"])['password']
    client = anthropic.Anthropic(
        base_url= profile["base_url"],
        api_key= api_key
    )
    model = model_name if model_name else profile["model"]
    print(f"llm profile name : {llm_profile_name} , model : {model}")
    return client , model