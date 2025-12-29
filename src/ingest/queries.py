GET_SERIES_FOR_TEAM = """
query GetSeriesForTeam($teamId: ID!, $first: Int) {
  series(filter: {teamIds: [$teamId]}, first: $first, orderBy: {direction: DESC, field: START_TIME}) {
    nodes {
      id
      startTime
      teams {
        id
        name
      }
      matches {
        id
        map {
          name
        }
      }
    }
  }
}
"""

GET_MATCH_DETAILS = """
query GetMatchDetails($matchId: ID!) {
  match(id: $matchId) {
    id
    startTime
    map {
      name
    }
    teams {
      id
      name
      side
    }
    artifacts {
      id
      type
      url
    }
  }
}
"""
