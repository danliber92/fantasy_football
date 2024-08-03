class base_league:
    def __init__(self,
         field_goal_short_dist, #distance for short fieldgoal
         field_goal_long_dist, #distance for long fieldgoal
         pa_0, #points allowed 0 cutoff
         pa_1, #points allowed 1 cutoff
         pa_2, #points allowed 2 cutoff
         pa_3, #points allowed 3 cutoff
         pa_4, #points allowed 4 cutoff
         pa_5, #points allowed 5 cutoff
         ):
        pass
    def set_offensive_points(self,
        reception, #point per reception
        running, #point per yard - run
        passing, #points per yard - pass
        receiving, #points per yard - receiving
        interception, #points lost per interception
        fumble, #points lost per fumble
        two_point_converstion, #points per 2 point conversion
        running_td, #points per running touchdown
        passing_td, #points per passing touchdown
        receiving_td, #points per receiving touchdown
        extra_point, #points per extra point kick made
        field_goal_short, #points per short fieldgoal
        field_goal_long #points per long fieldgoal
        ):
        pass
    def set_defensive_points(self,
         sack, #points per sack
         fumble_recover, #points per recovered fumble
         interception_caught, #points per interception caught
         safeties, #points per safety
         special_teams_touchdown, #points per kickoff/punt returned for touchdown
         defense_touchdown, #points per defensive touchdown
         points_allowed_0, #points for keeping offense to less than pa_0 points
         points_allowed_1, #points for keeping offense to less than pa_1 points
         points_allowed_2, #points for keeping offense to less than pa_2 points
         points_allowed_3, #points for keeping offense to less than pa_3 points
         points_allowed_4, #points for keeping offense to less than pa_4 points
         points_allowed_5, #points for keeping offense to less than pa_5 points
         ):
        pass
    