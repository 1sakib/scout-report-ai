import os
from typing import Any, Dict, List, Optional

import requests

from src.ingest.queries import GET_MATCH_DETAILS, GET_SERIES_FOR_TEAM


class GridClient:
    """Client for interacting with the GRID Esports Data API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GRID_API_KEY")
        self.base_url = "https://api.grid.gg/query"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _execute_query(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("GRID_API_KEY not found in environment or provided to client.")

        response = requests.post(
            self.base_url,
            json={"query": query, "variables": variables},
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def get_series_for_team(self, team_id: str, count: int = 10) -> List[Dict[str, Any]]:
        """Fetches recent series for a specific team."""
        variables = {"teamId": team_id, "first": count}
        result = self._execute_query(GET_SERIES_FOR_TEAM, variables)
        return result.get("data", {}).get("series", {}).get("nodes", [])

    def get_match_details(self, match_id: str) -> Dict[str, Any]:
        """Fetches detailed information for a specific match, including artifact URLs."""
        variables = {"matchId": match_id}
        result = self._execute_query(GET_MATCH_DETAILS, variables)
        return result.get("data", {}).get("match", {})

    def download_artifact(self, url: str) -> Dict[str, Any]:
        """Downloads a telemetry artifact (JSON) from the provided URL."""
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
