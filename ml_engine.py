import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

class MLEngine:
    def __init__(self, model_path="maestro_model.pkl"):
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
            except:
                self.model = None

    def prepare_features(self, df):
        """Transforma candles em dados que a IA entende."""
        # Criamos 'features' baseadas em indicadores
        df = df.copy()
        
        # RSI, Volatilidade, Distância de Médias, etc.
        # Precisamos garantir que os indicadores existam
        if 'rsi' not in df.columns: return None
        
        features = pd.DataFrame()
        features['rsi'] = df['rsi']
        features['rsi_fast'] = df['rsi_fast']
        features['atr_rel'] = df['atr'] / df['close']
        features['dist_sma'] = (df['close'] - df['sma_fast_9']) / df['close']
        features['vol_rel'] = df['tick_volume'] / df['vol_sma']
        
        return features.dropna()

    def train(self, df):
        """Aprende com o histórico passado."""
        # 1. Preparar Alvos (O que queremos prever?)
        # Vamos prever se o preço sobe (>0.1%) nos próximos 5 minutos
        df = df.copy()
        future_return = df['close'].shift(-5) / df['close'] - 1
        
        # Classe 1: Sobe, Classe 2: Desce, Classe 0: Neutro
        df['target'] = 0
        df.loc[future_return > 0.0005, 'target'] = 1 # Bullish
        df.loc[future_return < -0.0005, 'target'] = 2 # Bearish
        
        features = self.prepare_features(df)
        if features is None or len(features) < 100:
            return False, "Dados insuficientes para treinamento."
            
        X = features
        y = df.loc[features.index, 'target']
        
        # 2. Treinar Random Forest
        self.model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        self.model.fit(X, y)
        
        # 3. Salvar
        joblib.dump(self.model, self.model_path)
        return True, "IA atualizada com sucesso! Modelo 'Maestro' calibrado."

    def predict(self, df_last_row):
        """Dá o palpite da probabilidade do próximo movimento."""
        if self.model is None:
            return None
            
        features = self.prepare_features(df_last_row)
        if features.empty:
            return None
            
        pred = self.model.predict(features.tail(1))
        prob = self.model.predict_proba(features.tail(1))
        
        classes = {0: "LATERAL", 1: "ALTA", 2: "BAIXA"}
        return {
            "prediction": classes[pred[0]],
            "confidence": np.max(prob) * 100
        }
