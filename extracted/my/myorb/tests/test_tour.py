from conftest import PASSWORD, MakeClient, complete_setup


def test_setup_leads_to_the_tour_of_a_made_up_day(make_client: MakeClient):
    client = make_client()
    complete_setup(client, tour=True)
    page = client.get("/").text
    assert "/static/tour.js" in page and "/static/driver.js" in page
    assert "Tour <span" in page
    assert ', <span class="greeting-name">Tony</span>' in page
    # Signing out stays with this myOrb, not the demo.
    assert 'action="/logout"' in page


def test_nothing_changes_during_the_tour(make_client: MakeClient):
    client = make_client()
    complete_setup(client, tour=True)
    response = client.post("/tasks", data={"text": "Water plants"})
    assert response.status_code == 403
    assert "the tour's made-up day" in response.text
    client.post("/tour/finish")
    assert "Water plants" not in client.get("/welcome/widgets").text


def test_the_tour_shows_only_to_whoever_is_signed_in(make_client: MakeClient):
    client = make_client()
    complete_setup(client, tour=True)
    client.cookies.clear()
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"].startswith("/login")


def test_finishing_the_tour_leads_to_get_started_with_own_data(make_client: MakeClient):
    client = make_client()
    complete_setup(client, tour=True)
    response = client.post("/tour/finish")
    assert response.url.path == "/integrations"
    assert "Get started" in response.text
    assert "Take the tour again" in response.text
    page = client.get("/").text
    assert "/static/tour.js" not in page and "Tony" not in page


def test_the_tour_stays_until_it_is_ended(make_client: MakeClient):
    client = make_client()
    complete_setup(client, tour=True)
    # A restart, signing in again.
    again = make_client()
    again.post("/login", data={"password": PASSWORD})
    assert "/static/tour.js" in again.get("/").text


def test_the_tour_can_be_taken_again(client):
    assert "/static/tour.js" not in client.get("/").text
    response = client.post("/tour/start")
    assert response.url.path == "/"
    assert "/static/tour.js" in response.text
