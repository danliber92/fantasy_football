alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

wr_advanced_stats_mappings = {'receiving':{'tgt':'pass_targets',
                                           'rec':'receptions',
                                           'yds':'receiving_yards',
                                           'td':'receiving_touchdowns',
                                           '1d':'first_down_receptions',
                                           'ybc':'yards_before_catch',
                                           'ybc/r':'yards_before_catch_per_reception',
                                           'yac':'yards_after_catch',
                                           'yac/r':'yards_after_catch_per_reception',
                                           'adot':'average_target_depth', #completed or not
                                           'bkrtkl':'broken_tackles',
                                           'rec/br':'reception_per_broken_tackle',
                                           'drop':'dropped_passes',
                                           'drop%':'dropped_passes_per_target',
                                           'int':'interceptions_on_target',
                                           'rat':'passer_rating_when_targeted'}}

wr_stats_mappings = {'receiving':{'tgt':'pass_targets',
                                  'rec':'receptions',
                                  'yds':'receiving_yards',
                                  'y/r':'receiving_yards_per_reception',
                                  'td':'receiving_touchdowns',
                                  'ctch%':'catch_percentage',
                                  'y/tgt':'receiving_yards_per_target'},
                     'scoring':{'td':'all_touchdowns',
                                'pts':'total_points_scored'},
                     'off._snaps':{'pct':'offensive_snap_percentage'},
                     'def._snaps':{'pct':'defensive_snap_percentage'},
                     'st_snaps':{'pct':'special_team_snap_percentage'}}

qb_stats_mapping = {'cmp':'passes_completed',
                    'att':'passes_attempted',
                    'comp%':'percent_completed_passes',
                    'yds':'passing_yards',
                    'td':'passing_touchdowns',
                    'td%':'percent_touchdown_per_pass',
                    'int':'interceptions_thrown',
                    'int%':'percent_interceptions_per_pass',
                    '1d':'first_down_passes',
                    'succ%':''}