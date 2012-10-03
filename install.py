#!/usr/bin/env python
# coding=utf-8

def install():
    # --- STEP 1 -----------
    import requests
    from django.utils.encoding import smart_str

    DEBUG = True
    FILES = ['http://www.bundesliga.de/js/matchdetails/matchdetails_liga_%02d.js' % i for i in range(1, 35)]

    with open('spielplan.py', 'w+') as target:
        target.write('# coding=utf-8\n')
        target.write('matchdetails = {}\n')
        for f in FILES:
            if DEBUG:
                print('Fetching %s' % f)
            for line in smart_str(requests.get(f).text).split('\n')[1:]:
                if not line.startswith('matchdetails = new Array();'):
                        target.write('%s\n' % (line.replace(';', '').replace('new Array()', '{}')))

    if DEBUG:
        print('Finished generating spielplan.py')



    # --- STEP 2 -----------
    from spielplan import matchdetails

    matches = []
    teams = {}

    for key, match in matchdetails.items():
        matches.append({
            'team_home_handle': match['teamname_home_lettercode'],
            'team_home_name': match['teamname_home'],
            'team_visitor_handle': match['teamname_guest_lettercode'],
            'team_visitor_name': match['teamname_guest'],
            'timestamp': float(match['match_timestamp']),
            'matchday': int(match['matchday'])
        })
        if not teams.has_key(match['teamname_home_lettercode']):
            teams[match['teamname_home_lettercode']] = match['teamname_home']        

    if DEBUG:
        print('Finished extracting important information.')

    sorted_matches = sorted(matches, key=lambda k: '%02d %f' % (int(k['matchday']), k['timestamp'])) 

    """
    for match in sorted_matches:
        print('%s;%s;%f;%d' % (
            match['matchday'],
            match['timestamp'],
            match['team_home_handle'],
            match['team_visitor_handle']
        ))

    for key, val in teams.items():
        print('%s: %s' % (key, val))
    """



    # --- STEP 3 -----------
    from tippspiel.models import Team, Match
    from datetime import datetime
    import pytz

    tz_berlin = pytz.timezone("Europe/Berlin")

    for handle, name in teams.items():
        t, created = Team.objects.get_or_create(handle=handle, defaults={'name': name})
        if created:
            t.save()
        if DEBUG:
            if created:
                print('Inserted team %s.' % name)
            else:
                print('Team %s already exists.' % name)

    if DEBUG:
        print('Finished inserting teams.')

    for match in sorted_matches:
        date = datetime.fromtimestamp(match['timestamp'])
        date.replace(tzinfo=tz_berlin)
        matchday = match['matchday']
        team_home=Team.objects.get(handle=match['team_home_handle'])
        team_visitor=Team.objects.get(handle=match['team_visitor_handle'])

        m, created = Match.objects.get_or_create(
            matchday=matchday,
            team_home=team_home,
            team_visitor = team_visitor,
            defaults = {
                'date': date
            }
        )
        if not created:
            m.date = date

        m.save()

        if DEBUG:
            if created:
                print('Inserted match %s' % m)
            else:
                print('Updated match %s' % m)

    if DEBUG:
        print('Finished inserting/updating matches.')



    # --- STEP 4 -----------
    from os import remove
    remove('spielplan.py')
    if DEBUG:
        print('Removed spielplan.py')

    if DEBUG:
        print('Done!')



if __name__ == '__main__':
    print("This should only be run via django's ./manage.py shell.")

