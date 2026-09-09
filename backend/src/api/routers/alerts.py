from fastapi import APIRouter, Depends

from src.api.dependencies import get_alert_service
from src.schemas import AlertItem
from src.services.alert import AlertService


router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=list[AlertItem])
async def list_alerts_view(alert_service: AlertService = Depends(get_alert_service)):
    return await alert_service.list_alerts()