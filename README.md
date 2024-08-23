# Superforecasters Only

After getting upset that manifold markets wasn't giving me good predictions on questions I cared about, user @mongo suggested I track only the forecasters that have good records. this is a cli to make that easy.

- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Examples](#examples)
- [Coming Soon](#coming-soon)
- [License](#license)

### Requirements

You need Python installed and a Manifold Markets API key.

The instructions below are for MacOS and Linux.

If you're on Windows, use WSL or figure it out yourself...

### Setup

1. Clone the repo
2. `python3 -m venv .venv`
3. `source .venv/bin/activate`
4. `pip install -r requirements.txt`

### Usage


positional arguments:
  {search-market,slug}  Available commands


    search-market       Search for a market and get user's position


    slug                Get market by slug and get user's position

### Examples: 

```bash
python3 main.py search-market "will we land on the moon next year" --user "SemioticRivalry"
```

This will interactively show you up to 10 markets that match your query. and you can select one to get the superforecaster of your choice's position.

```bash
python3 main.py slug "will-we-land-on-the-moon-next-year" --user "SemioticRivalry"
```

This will only work if the slug is valid (the slug is the last part of the url), so you must know the actual slug.
This will get the superforecaster of your choice's position non-interactively.

### Coming Soon

I hope to add functionality soon to get positions for multiple superforecasters.


### License

GPL-3 see LICENSE.txt



