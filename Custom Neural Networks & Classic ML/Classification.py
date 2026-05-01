import pandas as pd
import numpy as np

class NeuralNetworkClassification:
    def __init__(self, layer_sizes, learning_rate=0.01, activation='sigmoid'):
        self.layer_sizes = layer_sizes
        self.learning_rate = learning_rate
        self.activation = activation
        
        self.weights = []
        self.biases = []
        
        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * np.sqrt(2. / layer_sizes[i])
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    def act_fn(self, z):
        if self.activation == 'sigmoid':
            return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
        elif self.activation == 'relu':
            return np.maximum(0, z)
        elif self.activation == 'tanh':
            return np.tanh(z)
        else:
            return z

    def act_deriv(self, a, z):
        if self.activation == 'sigmoid':
            return a * (1 - a)
        elif self.activation == 'relu':
            return (z > 0).astype(float)
        elif self.activation == 'tanh':
            return 1 - a**2
        else:
            return np.ones_like(z)

    def sigmoid_output(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

    def forward(self, X):
        self.a = [X]
        self.z = []
        
        curr_a = X
        for i in range(len(self.weights) - 1):
            curr_z = np.dot(curr_a, self.weights[i]) + self.biases[i]
            curr_a = self.act_fn(curr_z)
            self.z.append(curr_z)
            self.a.append(curr_a)
            
        curr_z = np.dot(curr_a, self.weights[-1]) + self.biases[-1]
        curr_a = self.sigmoid_output(curr_z)
        self.z.append(curr_z)
        self.a.append(curr_a)
        
        return curr_a

    def backward(self, X, y):
        m = X.shape[0]
        dw = [np.zeros_like(w) for w in self.weights]
        db = [np.zeros_like(b) for b in self.biases]
        
        dz = self.a[-1] - y
        dw[-1] = (1/m) * np.dot(self.a[-2].T, dz)
        db[-1] = (1/m) * np.sum(dz, axis=0, keepdims=True)
        
        for i in range(len(self.weights) - 2, -1, -1):
            da = np.dot(dz, self.weights[i+1].T)
            dz = da * self.act_deriv(self.a[i+1], self.z[i])
            dw[i] = (1/m) * np.dot(self.a[i].T, dz)
            db[i] = (1/m) * np.sum(dz, axis=0, keepdims=True)
            
        for i in range(len(self.weights)):
            self.weights[i] -= self.learning_rate * dw[i]
            self.biases[i] -= self.learning_rate * db[i]

    def train(self, X, y, epochs):
        for _ in range(epochs):
            self.forward(X)
            self.backward(X, y)

    def predict(self, X):
        probs = self.forward(X)
        return (probs >= 0.5).astype(int)

def load_and_prep_data(filepath):
    df = pd.read_csv(filepath, sep=';', decimal=',')
    
    for col in df.columns:
        if df[col].dtype == 'object' and col != 'Data':
            df[col] = df[col].str.replace(',', '.').astype(float)
            
    X = df.drop(columns=['Data', 'Target_Regresja', 'Target_Klasyfikacja']).values
    y = df['Target_Klasyfikacja'].values.reshape(-1, 1) 
    
    return X, y

def run_classification_experiment(X, y, test_split, layers, lr, activation, epochs, repeats=5):
    split_idx = int(len(X) * (1 - test_split))
    X_train_raw, X_test_raw = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    X_mean, X_std = np.mean(X_train_raw, axis=0), np.std(X_train_raw, axis=0)
    X_std[X_std == 0] = 1e-8
    
    X_train = (X_train_raw - X_mean) / X_std
    X_test = (X_test_raw - X_mean) / X_std
    
    train_accs = []
    test_accs = []
    
    for r in range(repeats):
        nn = NeuralNetworkClassification(layer_sizes=layers, learning_rate=lr, activation=activation)
        nn.train(X_train, y_train, epochs)
        
        y_train_pred = nn.predict(X_train)
        y_test_pred = nn.predict(X_test)
        
        acc_train = np.mean(y_train_pred == y_train) * 100
        acc_test = np.mean(y_test_pred == y_test) * 100
        
        train_accs.append(acc_train)
        test_accs.append(acc_test)
        
    avg_train = np.mean(train_accs)
    best_train = np.max(train_accs) 
    avg_test = np.mean(test_accs)
    best_test = np.max(test_accs)
    
    return avg_train, best_train, avg_test, best_test

if __name__ == "__main__":
    print("Ładowanie danych do klasyfikacji...")
    X, y = load_and_prep_data('xauusd_dla_excela.csv')
    input_size = X.shape[1]
    
    base_layers = [input_size, 20, 1]
    base_lr = 0.01
    base_epochs = 1000
    base_split = 0.2
    base_act = 'sigmoid'
    
    experiments = {
        "1. Liczba neuronów w warstwie ukrytej": [
            ([input_size, 5, 1], "5 neuronów"),
            ([input_size, 10, 1], "10 neuronów"),
            ([input_size, 20, 1], "20 neuronów"),
            ([input_size, 50, 1], "50 neuronów")
        ],
        "2. Współczynnik uczenia (Learning Rate)": [0.1, 0.01, 0.005, 0.001],
        "3. Liczba epok (Iteracji)": [500, 1000, 2000, 3000],
        "4. Funkcja aktywacji": ['sigmoid', 'relu', 'tanh', 'linear'],
        "5. Rozmiar próby testowej": [0.1, 0.2, 0.3, 0.4],
        "6. Liczba warstw ukrytych (po 10 neuronów)": [
            ([input_size, 10, 1], "1 warstwa"),
            ([input_size, 10, 10, 1], "2 warstwy"),
            ([input_size, 10, 10, 10, 1], "3 warstwy"),
            ([input_size, 10, 10, 10, 10, 1], "4 warstwy")
        ]
    }
    
    print("ROZPOCZYNANIE BADAŃ DLA KLASYFIKACJI (Wzrost/Spadek złota) \n")
    
    for exp_name, values in experiments.items():
        print(f"--- Badany parametr: {exp_name} ---")
        print(f"{'Wartość':<15} | {'Śr. ACC TRAIN':<15} | {'Najl. ACC TRAIN':<18} | {'Śr. ACC TEST':<15} | {'Najl. ACC TEST'}")
        print("-" * 88)
        
        for val in values:
            layers, lr, epochs, act, split, label = base_layers, base_lr, base_epochs, base_act, base_split, str(val)
            
            if "neuronów w warstwie" in exp_name: layers, label = val
            elif "Współczynnik uczenia" in exp_name: lr = val
            elif "epok" in exp_name: epochs = val
            elif "Funkcja aktywacji" in exp_name: act = val
            elif "Rozmiar próby" in exp_name: split, label = val, f"{int((1-val)*100)}% / {int(val*100)}%"
            elif "Liczba warstw" in exp_name: layers, label = val
                
            avg_tr, best_tr, avg_te, best_te = run_classification_experiment(X, y, split, layers, lr, act, epochs, repeats=5)
            
            print(f"{label:<15} | {avg_tr:<14.2f}% | {best_tr:<17.2f}% | {avg_te:<14.2f}% | {best_te:.2f}%")
        
        print("\n")
        
    print("\n--- OSTATECZNY TEST WYBRANEGO MODELU ---")
    optymalne_warstwy = [input_size, 50, 1]
    best_model = NeuralNetworkClassification(layer_sizes=optymalne_warstwy, learning_rate=0.01)
    
    split_index = int(len(X) * 0.8)
    X_train_raw, X_test_raw = X[:split_index], X[split_index:]
    y_train_final, y_test_final = y[:split_index], y[split_index:]
    
    X_mean, X_std = np.mean(X_train_raw, axis=0), np.std(X_train_raw, axis=0)
    X_std[X_std == 0] = 1e-8
    X_train_final = (X_train_raw - X_mean) / X_std
    X_test_final = (X_test_raw - X_mean) / X_std
    
    best_model.train(X_train_final, y_train_final, epochs=2000)
    
    fizyczne_prognozy = best_model.predict(X_test_final)
    
    print("\nWyniki dla pierwszych 20 dni z próby testowej:")
    print("--------------------------------------------------")
    print(f"{'Nr dnia':<10} | {'Prawdziwa sytuacja':<20} | {'Co przewidziała sieć'}")
    print("--------------------------------------------------")
    
    licznik = 0

    for i in range(min(20, len(y_test_final))):
        prawda = "Wzrost (1)" if y_test_final[i][0] == 1 else "Spadek (0)"
        prognoza = "Wzrost (1)" if fizyczne_prognozy[i][0] == 1 else "Spadek (0)"
        
        (trafienie, licznik) = ("DOBRZE", licznik + 1) if prawda == prognoza else ("ŹLE", licznik)
        print(f"Dzień {i+1:<4} | {prawda:<20} | {prognoza:<20} {trafienie}")
    print("\n")
    print(f"Łączna liczba trafień: {licznik} na {min(20, len(y_test_final))} próbek testowych.")
        