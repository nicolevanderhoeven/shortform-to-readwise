# Shortform to Readwise

Work in progress!

This script scrapes [Shortform](https://www.shortform.com) for highlights and sends them to [Readwise](https://readwise.io). Accounts with both Shortform and Readwise are required.

## Usage

Enter the required data in `variables.py`.

`authToken` is the Authorization token that you use for Shortform. Shortform unfortunately doesn't expose this, but you can find out yours by opening up DevTools in Chrome or Firefox and navigating to, for example, [your highlights page](https://www.shortform.com/app/highlights). In the DevTools Network tab, look for the request with the name `?sort=date` and click on it. In the Request Headers panel, you'll see a header `Authorization`, with the value `Basic <your token>`. Copy everything after `Basic ` and paste it into `variables.py`. _(Note: There shouldn't be any spaces in the token.)_

`readwiseToken` is your API token for Readwise, which you can get [here](https://readwise.io/access_token)

Clone or download this repo, cd into it, and run the main script: `python3 gethighlights.py`

You should be able to see your highlights appear in [your Readwise library](https://readwise.io/books).

To run this script automatically, you can use crontab or similar.
