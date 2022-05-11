import unittest

import pandas
from dash_fpl.captain_picks import total_points_multiplier, dataframe_col_to_list, points_multiplier, \
    captain_points_difference, get_GW_captain_picks, match_captain_pick_to_score, multiply_by_3, \
    get_GW_optimal_captains, getGenericPlayerData, captain_points_to_col, dataframe_col_rename, \
    optimal_captain

from pandas.testing import assert_frame_equal, assert_series_equal
import pandas as pd


class TestCaptainMultiplier(unittest.TestCase):

    def test_points_multiplier_data_type(self):
        df = pd.DataFrame({
            'total_points': [5, 1, 16, 7],
            'multiplier': [1, 2, 1, 1]
        })
        expected = pd.Series([5, 2, 16, 7])

        actual = total_points_multiplier(df)
        self.assertEqual(type(expected), type(actual))

    def test_points_multiplier(self):
        df = pd.DataFrame({
            'total_points': [5, 2, 16, 7],
            'multiplier': [1, 2, 1, 1]
        })
        expected = pd.Series([5, 4, 16, 7])

        actual = total_points_multiplier(df)
        pd.testing.assert_series_equal(expected, actual)


class TestMultiplyPointsByThreeOrTwo(unittest.TestCase):

    def test_multiply_three(self):
        df = pd.DataFrame({
            'Player': ['Mount', 'Saka'],
            'multiplier': [3, 1]
        })
        expected = pd.DataFrame({
            'Player': ['Mount'],
            'multiplier': [3]
        })

        actual = multiply_by_3(df)
        pd.testing.assert_frame_equal(expected, actual)


class TestCaptainListConversion(unittest.TestCase):

    def test_dataframe_col_to_list_data_struct(self):
        df = pd.DataFrame({
            'element': ['Mount', 'Werner', 'Cornet']
        })
        expected = ['Mount', 'Werner', 'Cornet']

        actual = dataframe_col_to_list(df)
        self.assertEqual(type(expected), type(actual))

    def test_dataframe_col_to_list(self):
        df = pd.DataFrame({
            'element': ['Mount', 'Werner', 'Cornet']
        })
        expected = ['Mount', 'Werner', 'Cornet']
        actual = dataframe_col_to_list(df)
        self.assertEqual(expected, actual)


class TestPointsMultiplierForOptimalCaptains(unittest.TestCase):

    def test_multiplier_points_output_is_Series(self):
        df = pd.DataFrame({
            'points': [-3, -1, 0, 5, 10, 25]
        })
        expected = pd.Series([-6, -2, 0, 10, 20, 50], name='points')
        actual = points_multiplier(df)
        self.assertEqual(type(expected), type(actual))

    def test_points_multiplier(self):
        df = pd.DataFrame({
            'points': [-3, -1, 0, 5, 10, 25]
        })
        expected = pd.Series([-6, -2, 0, 10, 20, 50], name='points')
        actual = points_multiplier(df)
        pd.testing.assert_series_equal(expected, actual)


class TestTheDifferenceBetweenManagersCaptainAndOptimal(unittest.TestCase):

    def test_difference_between_points_data_struct(self):
        df = pd.DataFrame({
            'Points': [2, -2, 16, 2],
            'Optimal Points': [10, 7, 16, 7]
        })
        expected = pd.Series([-8, -9, 0, -5])
        actual = captain_points_difference(df)
        self.assertEqual(type(expected), type(actual))

    def test_difference_between_points(self):
        df = pd.DataFrame({
            'Points': [2, -2, 16, 2],
            'Optimal Points': [10, 7, 16, 7]
        })
        expected = pd.Series([-8, -9, 0, -5])
        actual = captain_points_difference(df)
        pd.testing.assert_series_equal(expected, actual)


# valid manager id and gameweek
class TestGameWeekCaptainPicksOfManager(unittest.TestCase):

    def test_invalid_manager_id(self):
        expectedDF = pd.DataFrame()
        expectedGameweek = 1
        managerID = 'asdr123'
        actualDF, actualGameWeek = get_GW_captain_picks(managerID, expectedGameweek, expectedDF)
        self.assertEqual(expectedGameweek, actualGameWeek)
        pd.testing.assert_frame_equal(expectedDF, actualDF)

    def test_invalid_gameweek(self):
        expectedDF = pd.DataFrame()
        invalidGameweekInput = 100
        expectedGameweek = 1
        managerID = '1'
        actualDF, actualGameWeek = get_GW_captain_picks(managerID, invalidGameweekInput, expectedDF)
        self.assertEqual(expectedGameweek, actualGameWeek)
        pd.testing.assert_frame_equal(expectedDF, actualDF)

    def test_data_types_and_structures(self):
        expectedDF = pd.DataFrame()
        expectedGameweek = 1
        managerID = 3
        actualDF, actualGameWeek = get_GW_captain_picks(managerID, expectedGameweek, expectedDF)
        self.assertEqual(type(expectedGameweek), type(actualGameWeek))
        self.assertEqual(type(expectedDF), type(actualDF))


class TestFindScoresForManagerCaptainPicksEachWeek(unittest.TestCase):

    def test_captain_gameweek_points_match(self):
        captains = [233]
        captain_points = []
        expectedCaptainPoints = [17]
        expectedGameweek = 1

        actualCaptainPoints, actualGameWeek = match_captain_pick_to_score(captains, captain_points, expectedGameweek)
        self.assertEqual(expectedGameweek, actualGameWeek)
        self.assertEqual(expectedCaptainPoints, actualCaptainPoints)

    def test_if_no_captain_TypeError(self):
        captains = []
        captain_points = []
        # expectedCaptainPoints =
        expectedGameweek = 1
        self.assertRaises(TypeError, match_captain_pick_to_score(captains, captain_points, expectedGameweek))

    def test_if_invalid_captain_returns_empty_list(self):
        captains = [1000]
        captain_points = []
        expectedCaptainPoints = []
        expectedGameweek = 1
        actualCaptainPoints, actualGameWeek = match_captain_pick_to_score(captains, captain_points, expectedGameweek)
        self.assertEqual(expectedCaptainPoints, actualCaptainPoints)

    def test_data_types(self):
        captains = [233]
        captain_points = []
        expectedCaptainPoints = [17]
        expectedGameweek = 1

        actualCaptainPoints, actualGameWeek = match_captain_pick_to_score(captains, captain_points, expectedGameweek)
        self.assertEqual(type(expectedGameweek), type(actualGameWeek))
        self.assertEqual(type(expectedCaptainPoints), type(actualCaptainPoints))


class TestGetGameweekOptimalCaptainFunction(unittest.TestCase):

    def test_invalid_gameweek(self):
        expectedDF = pd.DataFrame()
        gameweekInput = 40

        actualDF = get_GW_optimal_captains(expectedDF, gameweekInput)
        pd.testing.assert_frame_equal(expectedDF, actualDF)
        self.assertEqual(type(expectedDF), type(actualDF))

    def test_valid_gameweek(self):
        expectedDF = pd.DataFrame()
        gameweekInput = 1

        actualDF = get_GW_optimal_captains(expectedDF, gameweekInput)
        self.assertEqual(type(expectedDF), type(actualDF))


class TestGenericPlayerDataFunctionReturnTypes(unittest.TestCase):

    def test_generic_player_returns_a_dataframe(self):
        expectedDF = pd.DataFrame()
        actualDF = getGenericPlayerData()
        self.assertEqual(type(expectedDF), type(actualDF))


if __name__ == '__main__':
    unittest.main()
