from fastapi import APIRouter

router = APIRouter()

@router.get("/customer_data")
def get_profiles():
    return [
        {
            "distributor_name": "TechNova",
            "challenges": ["Onboarding delays", "Pricing confusion", "Lack of technical docs"]
        },
        {
            "distributor_name": "GlobalLink",
            "challenges": ["Enablement gaps", "Support response time"]
        }
    ]
