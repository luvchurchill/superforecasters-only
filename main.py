"""
Copyright (C) 2024  luvchurchill

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import argparse
import os
from typing import List, Dict, Any

import requests

API_BASE_URL = "https://api.manifold.markets/v0"
API_KEY = os.environ.get("MANIFOLD_API_KEY")

if API_KEY is None:
    raise ValueError("MANIFOLD_API_KEY environment variable not set.")


def _make_api_request(method: str, endpoint: str, data: dict = None) -> dict:
    headers = {
        "Authorization": f"Key {API_KEY}",
        "Content-Type": "application/json"
    }
    url = f"{API_BASE_URL}{endpoint}"

    if method == "GET":
        response = requests.get(url, headers=headers, params=data)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    return response.json()


def search_market(term: str, limit: int = 10) -> List[Dict]:
    """Search for a market by term and return a list of matching markets."""
    data = {"term": term, "limit": limit}
    return _make_api_request("GET", "/search-markets", data=data)


def get_market_by_slug(market_slug: str) -> Dict:
    """Get market information by its slug."""
    return _make_api_request("GET", f"/slug/{market_slug}")


def get_user_by_username(username: str) -> Dict:
    """Get user information by their username."""
    return _make_api_request("GET", f"/user/{username}")


def get_bets(user_id: str, contract_id: str) -> List[Dict]:
    """Get a user's bets on a specific market."""
    data = {
        "userId": user_id,
        "contractId": contract_id,
    }
    return _make_api_request("GET", "/bets", data=data)

def get_market_by_id(market_id: str):
    """Get market information by its slug."""
    return _make_api_request("GET", f"/market/{market_id}")


def get_user_position_in_market(market_id: str, username: str) -> str:
    """
    Get a user's position in a specific market.

    Args:
      market_id: The ID of the market.
      username: The username of the user.

    Returns:
      A string describing the user's position.
    """
    user = get_user_by_username(username)
    user_id = user['id']

    # Fetch the complete market data to handle multiple-choice markets correctly
    market = get_market_by_id(market_id)
    bets = get_bets(user_id, market_id)

    total_shares = {}  # Use a dictionary to track shares per outcome
    for bet in bets:
        outcome = bet['outcome']
        if outcome not in total_shares:
            total_shares[outcome] = 0
        total_shares[outcome] += bet['shares']

    if not total_shares:  # Check if the dictionary is empty
        return f"{username} has no position in this market."

    position_strings = []
    for outcome_binary, shares in total_shares.items():
        outcome = outcome_binary  
        if market['outcomeType'] == 'MULTIPLE_CHOICE':
            for answer in market['answers']:
                if answer['id'] == bet["answerId"]:
                    position_strings.append(f"{shares:.2f} {outcome_binary} on {answer['text']}")
                    break
        else:
            position_strings.append(f"{shares:.2f} on {outcome_binary}")

    return f"{username} bet " + ', '.join(position_strings)  # Join the positions

def main():
    parser = argparse.ArgumentParser(description="Manifold CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Search Market and User Position
    search_parser = subparsers.add_parser("search-market", help="Search for a market and get user's position")
    search_parser.add_argument("term", type=str, help="Search term for the market")
    search_parser.add_argument("--user", type=str, required=True, help="Username of the user")

    # Slug and User Position
    slug_parser = subparsers.add_parser("slug", help="Get market by slug and get user's position")
    slug_parser.add_argument("slug", type=str, help="Market slug")
    slug_parser.add_argument("--user", type=str, required=True, help="Username of the user")

    args = parser.parse_args()

    if args.command == "search-market":
        markets = search_market(args.term)
        if markets:
            for i, market in enumerate(markets):
                print(f"{i+1}. {market['question']}")

            choice = int(input("Enter the number of the market you're interested in: ")) - 1
            selected_market = markets[choice]
            market_id = selected_market['id']

            position = get_user_position_in_market(market_id, args.user)
            print(position)
        else:
            print("No markets found matching that term.")

    elif args.command == "slug":
        try:
            market = get_market_by_slug(args.slug)
            market_id = market['id']
            position = get_user_position_in_market(market_id, args.user)
            print(position)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Market with slug '{args.slug}' not found.")
            else:
                raise

if __name__ == "__main__":
    main()