import numpy as np
from scipy.stats import f

class ARLCalculator:
    @staticmethod
    def carta_control_t2(x, xvar, S_inv, n):
        """
        Calculate the T2 statistic for a given observation.
        Parameters:
        x (numpy.ndarray): The observation vector.
        xvar (numpy.ndarray): The mean vector of the process.
        S_inv (numpy.ndarray): The inverse of the covariance matrix of the process.
        n (int): The sample size.
        Returns:
        float: The T2 statistic.
        """
        
        return n * np.dot(np.dot((x - xvar).T, S_inv), (x - xvar))

    @staticmethod
    def contar_puntos_sintetico(t2, lcs, l):
        """
        Calculate synthetic points based on given thresholds.
        This function iterates over the list `t2` and checks if each element exceeds the threshold `lcs`.
        If an element exceeds the threshold, its index is added to the `arl` list. Additionally, if the 
        difference between the current index and the last added index in `arl` is less than `l`, the index 
        is also added to the `crl` list.
        Args:
            t2 (list): A list of numerical values to be evaluated.
            lcs (float): The threshold value to compare against elements in `t2`.
            l (int): The minimum difference between indices to be considered for `crl`.
        Returns:
            tuple: A tuple containing two lists:
                - crl (list): List of indices where the difference between consecutive indices in `arl` is less than `l`.
                - arl (list): List of indices where elements in `t2` exceed the threshold `lcs`.
        """
        
        arl = [0]
        crl = [0]
        for i in range(len(t2)):
            if t2[i] > lcs:
                arl.append(i)
                if i - arl[-2] < l:
                    crl.append(i)
        return crl, arl

    def calculate_arl(self, m, n, p, Delta, L, alpha=None, LCynt=None):
        """
        Calculate the Average Run Length (ARL) and other related metrics for a given set of parameters.
        Parameters:
        m (int): Number of samples.
        n (int): Sample size.
        p (int): Number of variables.
        Delta (float): Shift in the mean vector.
        L (int): Length of the control chart.
        alpha (float, optional): Significance level for the control limit. Default is None.
        LCynt (float, optional): Predefined control limit. Default is None.
        Returns:
        dict: A dictionary containing:
            - 'CRL' (float): The mean of the differences between consecutive run lengths.
            - 'CRL_INTERCALADO' (float): The mean of the differences between every second run length, scaled by 1.4.
        np.ndarray: Array of T2 values.
        np.ndarray: Array of differences between ARL points.
        float: Calculated or provided control limit (LCynt).
        """
        
        mean = np.zeros(p)
        mean[-1] = Delta
        cov1 = np.eye(p)
        invcov = np.linalg.inv(cov1)

        data = np.random.multivariate_normal(mean, cov1, (m, n))
        meansv = np.mean(data, axis=1)
        t2_values = np.array([
            self.carta_control_t2(x, np.zeros(p), invcov, n) for x in meansv
        ])

        if LCynt is None and alpha is not None:
            LCynt = ((n - 1) * p / (n - p)) * f.ppf(1 - alpha, p, n - p)
        elif LCynt is None:
            LCynt = ((n - 1) * p / (n - p)) * f.ppf(1 - 0.05, p, n - p)

        crl_points, arl_points = self.contar_puntos_sintetico(t2_values, LCynt, L)
        arl_points = np.diff(arl_points)

        crl_intercalado_mean = (
            np.mean([crl_points[i + 2] - crl_points[i] for i in range(len(crl_points) - 2)]) * 1.4
            if len(crl_points) > 2 else np.nan
        )

        crl = np.mean(np.diff(crl_points)) if len(crl_points) > 1 else np.nan

        return {
            'CRL': crl,
            'CRL_INTERCALADO': crl_intercalado_mean
        }, t2_values, arl_points, LCynt
