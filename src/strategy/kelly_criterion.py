# src/strategy/kelly_criterion.py

class KellyCalculator:
    def __init__(self, fraction: float = 0.25, max_bet_pct: float = 0.10):
        """
        :param fraction: Fractional multiplier (0.25 = Quarter Kelly). Safer than full Kelly.
        :param max_bet_pct: Maximum portfolio percentage per single bet (safety cap).
        """
        self.fraction = fraction
        self.max_bet_pct = max_bet_pct

    def calculate_bet_amount(self, bankroll: float, price: float, estimated_prob: float) -> float:
        """
        Calculate the bet amount in USDC.
        """
        if estimated_prob <= price:
            return 0.0  # No edge means no bet

        b = (1.0 / price) - 1.0 # 1. Calculate net odds (b)
        p = estimated_prob
        q = 1.0 - p
        f_star = (b * p - q) / b # 2. Kelly formula
        # 3. Apply Fractional Kelly and a safety cap
        bet_fraction = f_star * self.fraction 
        # Never bet more than max_bet_pct of bankroll
        final_fraction = min(bet_fraction, self.max_bet_pct)
        
        return max(0.0, bankroll * final_fraction)