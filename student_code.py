def decrypt(C):
  M=""
  #entrez votre code ici.
  #Vous pouvez créer des fonctions auxiliaires et adapter le code à votre façon mais decrypt dois renvoyer le message décrypté


  def cut_string_into_pairs(text):
    """
    Découpe la chaîne de caractères en paires de caractères.
    Si le nombre de caractères est impair, ajoute un caractère de remplissage "_".
    """
    pairs = [text[i:i + 2] for i in range(0, len(text) - 1, 2)]
    if len(text) % 2 != 0:
        pairs.append(text[-1] + '_')  # Ajouter un "_" pour les chaînes impaires
    return pairs

  def load_text_from_web(url):
    """
    Charge le texte à partir d'une URL donnée et retourne le contenu en texte brut.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du chargement du texte : {e}")
        return None

  def split_into_8bit_chunks(text):
    """
    Divise le texte en blocs de 8 bits pour chaque symbole.
    """
    return [text[i:i+8] for i in range(0, len(text), 8)]

  def calculate_symbol_frequencies(bit_chunks):
    """
    Calcule les fréquences de chaque bloc de 8 bits.
    Retourne un dictionnaire trié par fréquence décroissante.
    """
    compte_symboles = Counter(bit_chunks)
    total_symboles = sum(compte_symboles.values())
    return {symbole: (compte / total_symboles) * 100 for symbole, compte in compte_symboles.most_common()}

  def get_french_frequencies():
    """
    Calcule les fréquences des symboles et paires de caractères fréquents dans un texte français.
    """
    url = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"  # Example URL (replace with your desired URL)
    text = load_text_from_web(url)
    url = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"  # Example URL (replace with your desired URL)
    text = text + load_text_from_web(url)

    caracteres = list(text)
    bicaracteres = cut_string_into_pairs(text)
    symboles = caracteres + bicaracteres

    compte_symboles = Counter(symboles)
    total_symboles = sum(compte_symboles.values())
    return {symbole: (compte / total_symboles) * 100 for symbole, compte in compte_symboles.most_common()}

  def associer_symboles_les_plus_proches(dico1, dico2):
    """
    Associe les symboles de dico1 aux symboles de dico2 avec les fréquences les plus proches.
    """
    associations = {}
    dico2_copie = dico2.copy()

    for symbole1, pourcentage1 in dico1.items():
        symbole_proche = min(dico2_copie, key=lambda symbole2: abs(dico2_copie[symbole2] - pourcentage1))
        associations[symbole1] = symbole_proche
        del dico2_copie[symbole_proche]  # Empêche les doublons

    return associations

  def decrypt_with_key(bit_chunks, substitution_key):
    """
    Déchiffre les blocs de 8 bits en utilisant une clé de substitution.
    Remplace par '?' si la clé n'existe pas.
    """
    return ''.join(substitution_key.get(bits, '?') for bits in bit_chunks)


# Diviser le texte chiffré en blocs de 8 bits
  bit_chunks = split_into_8bit_chunks(C)
  bit_chunks_freq = calculate_symbol_frequencies(bit_chunks)

# Obtenir les fréquences des symboles en français
  frequent_chars = get_french_frequencies()


# Dériver la clé de substitution à partir des blocs de 8 bits
  substitution_key = associer_symboles_les_plus_proches(bit_chunks_freq, frequent_chars)

# Décoder le texte
  M = decrypt_with_key(bit_chunks, substitution_key)

  return M
