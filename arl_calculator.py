import numpy as np
from scipy.stats import f

class ARLCalculator:
    @staticmethod
    def carta_control_t2(x, xvar, S_inv, n):
        return n * np.dot(np.dot((x - xvar).T, S_inv), (x - xvar))

    @staticmethod
    def contar_puntos_sintetico(t2, lcs, l):
        arl = [0]
        crl = [0]
        for i in range(len(t2)):
            if t2[i] > lcs:
                arl.append(i)
                if i - arl[-2] < l:
                    crl.append(i)
        return crl, arl

    def calculate_arl(self, m, n, p, Delta, L, alpha=None, LCynt=None):
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

        arl_intercalado_mean = (
            np.mean([crl_points[i + 2] - crl_points[i] for i in range(len(crl_points) - 2)]) * 1.4
            if len(crl_points) > 2 else np.nan
        )

        arl = np.mean(np.diff(crl_points)) if len(crl_points) > 1 else np.nan

        return {
            'ARL': arl,
            'ARL_Intercalado': arl_intercalado_mean
        }, t2_values, arl_points, LCynt
