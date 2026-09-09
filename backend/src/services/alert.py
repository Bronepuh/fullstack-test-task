from src.models import Alert
from src.repositories.alert import AlertRepository


class AlertService:
    def __init__(self, alert_repo: AlertRepository):
        self.alert_repo = alert_repo

    async def list_alerts(self) -> list[Alert]:
        return await self.alert_repo.get_all()