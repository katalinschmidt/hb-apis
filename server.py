import pprint
from flask import Flask, render_template, request

from pprint import pformat
import os
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['TICKETMASTER_KEY']#get the environment variable ticketmaster_key
#but the key needs to be secret so we're storing it in secrets.sh
# API_KEY = os.environ['BK6W6CAzfamgPNSdFMFsmTCwEq2uqYVr']


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/afterparty')
def show_afterparty_form():
    """Show event search form"""

    return render_template('search-form.html')


@app.route('/afterparty/search')
def find_afterparties():
    """Search for afterparties on Eventbrite"""

    keyword = request.args.get('keyword', '')
    postalcode = request.args.get('zipcode', '')
    radius = request.args.get('radius', '')
    unit = request.args.get('unit', '')
    sort = request.args.get('sort', '')

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey' : API_KEY, 'postalcode' : 'zipcode'}
    # payload = {'apikey': BK6W6CAzfamgPNSdFMFsmTCwEq2uqYVr}

    # - Make a request to the Event Search endpoint to search for events
    res = requests.get(url, params=payload)
    # print(res) #should produce <response[200]>
    # print(res.url)

    # - Use form data from the user to populate any search parameters

    # - Save the JSON data from the response to the `data` variable so it can display.
    data = res.json()
    # print(data) # Outputs Python dict
    # data # Outputs nothing

    events = data['_embedded']['events']
    # print(events) # Outputs huge JSON / Python dict

    event = events[0]
    # print(event)
    # pprint.pprint(event)

    # - Replace the empty list in `events` with the list of events from your search results


    data = {'Test': ['This is just some test data'],
            'page': {'totalElements': 1}}
    events = []

    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=events)


# ===========================================================================
# FURTHER STUDY
# ===========================================================================


@app.route('/event/<id>')
def get_event_details(id):
    """View the details of an event."""

    # TODO: Finish implementing this view function

    return render_template('event-details.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
