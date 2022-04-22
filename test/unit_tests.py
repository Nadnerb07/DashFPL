import unittest
from dash_fpl.captain_picks import total_points_multiplier, dataframe_col_to_list, points_multiplier, captain_points_difference
from pandas.testing import assert_frame_equal, assert_series_equal
import pandas as pd


class TestCaptainMultiplier(unittest.TestCase):

    def test_points_multiplier_input(self):
        df = pd.DataFrame({
            'total_points': [5, 1, 16, 7],
            'multiplier': [2, 3, 2, 2]
        })
        expected = pd.Series([10, 3, 32, 14])

        actual = total_points_multiplier(df)
        self.assertEqual(type(expected), type(actual))

    def test_points_multiplier(self):
        df = pd.DataFrame({
            'total_points': [5, 1, 16, 7],
            'multiplier': [2, 3, 2, 2]
        })
        expected = pd.Series([10, 3, 32, 14])

        actual = total_points_multiplier(df)
        pd.testing.assert_series_equal(expected, actual)


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

    def test_difference_between_points(self):
        df = pd.DataFrame({
            'Points': [2, -2, 16, 7],
            'Optimal Points': [10, 7, 2, 2]
        })
        expected = pd.Series([8, 5, 14, 4])
        actual = captain_points_difference(df)

if __name__ == '__main__':
    unittest.main()
