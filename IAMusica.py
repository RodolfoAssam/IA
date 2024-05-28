# Rodolfo Zahir Assam Méndez 19100794
# Utilizo 4 IAS:
# Síntesis de Voz:
# Utilizo gTTS (Google Text-to-Speech): 
# para convertir texto a voz y así puedo generar archivos de audio a partir de texto.

# Procesamiento de Lenguaje Natural (NLP): Utilizo scikit-learn para la clasificación de texto, 
# permitiéndome entrenar un modelo de clasificación que predice la categoría (motivacional, tristeza, risa) 
# de una frase ingresada por el usuario.

# Utilizo nltk (Natural Language Toolkit) para el manejo de palabras vacías (stopwords), 
# lo que mejora la precisión del modelo de clasificación de texto eliminando palabras comunes y no informativas.
# Reducción del Ruido, Eficiencia, Mejora en la Precisión
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import time
from midiutil.MidiFile import MIDIFile 
# Biblioteca midiutil se usa para crear y manipular archivos MIDI
from gtts import gTTS
# Se usa para convertir texto a voz utilizando Google Text-to-Speech (IA)
import pygame
# Se usa para reproducir audio y trabajar con multimedia en Python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
# Machine Learning Sklearn
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

class MidiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IA Musical")

        # Configurar la ventana principal
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Entrenar el modelo de clasificación de texto
        self.model = self.train_text_classifier()

        # Crear widgets
        self.create_widgets()

    def create_widgets(self):
        # Entrada de usuario
        self.user_input_label = ttk.Label(self.main_frame, text="Ingrese el tipo de frase que desea (motivacional, tristeza, risa):")
        self.user_input_label.grid(row=0, column=0, pady=5)
        self.user_input_entry = ttk.Entry(self.main_frame, width=50)
        self.user_input_entry.grid(row=1, column=0, pady=5)

        self.generate_button = ttk.Button(self.main_frame, text="Generar y Reproducir", command=self.generate_and_play)
        self.generate_button.grid(row=2, column=0, pady=10)

    def train_text_classifier(self):
        # Conjunto de datos entrenados
        self.train_data = [
            ("El éxito es la suma de pequeños esfuerzos repetidos día tras día", "motivacional"),
            ("Nunca es demasiado tarde para ser lo que podrías haber sido", "motivacional"),
            ("La vida es como una cámara, enfócate en lo importante y captura los buenos momentos", "motivacional"),
            ("La tristeza es un refugio seguro en el que encontramos consuelo", "tristeza"),
            ("A veces, el dolor es tan grande que solo el tiempo puede curarlo", "tristeza"),
            ("¿Por qué los peces no van a la escuela? Porque ya están en la corriente", "risa"),
            ("¿Qué hace una abeja en el gimnasio? ¡Zum-ba!", "risa"),
            ("El éxito no es la clave de la felicidad. La felicidad es la clave del éxito", "motivacional"),
            ("Cree en la magia de los nuevos comienzos", "motivacional"),
            ("Cuando una puerta se cierra, otra se abre", "motivacional"),
            ("La tristeza es el jardín donde crece la compasión", "tristeza"),
            ("Permítete sentir la tristeza y luego libérala", "tristeza"),
            ("¿Por qué los esqueletos no luchan entre ellos? Porque no tienen agallas", "risa"),
            ("¿Qué hace un pez en la oficina? Trabaja con el mouse", "risa")
        ]

        texts, labels = zip(*self.train_data)

        # Crear un pipeline de clasificación de texto
        model = make_pipeline(CountVectorizer(stop_words=stopwords.words('spanish')), MultinomialNB())

        # Entrenar el modelo
        model.fit(texts, labels)

        return model
    
        # IA Piano
    def piano_base(self, num_notes, min_pitch, max_pitch, min_duration, max_duration):
        # Crear el objeto MIDIFile
        MyMIDI = MIDIFile(1)

        # Añadir nombre de pista y tempo
        track = 0
        current_time = 0
        MyMIDI.addTrackName(track, current_time, "Random MIDI Track")
        MyMIDI.addTempo(track, current_time, 120)

        for _ in range(num_notes):
            channel = 0
            pitch = random.randint(min_pitch, max_pitch)
            duration = random.uniform(min_duration, max_duration)
            volume = 100
            MyMIDI.addNote(track, channel, pitch, current_time, duration, volume)
            current_time += duration

        # Escribir a archivo
        with open("output.mid", "wb") as binfile:
            MyMIDI.writeFile(binfile)

    def play_music(self, music_file):
        pygame.mixer.init()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()

        #IA Voz
    def text_to_speech(self, prompt):
        tts = gTTS(text=prompt, lang='es')
        tts.save("prompt.mp3")

    def play_prompt(self, prompt_file):
        pygame.mixer.init()
        prompt_sound = pygame.mixer.Sound(prompt_file)
        prompt_sound.play()

    def get_prompt(self, choice):
        # Filtrar las frases según la categoría elegida
        if choice in ["motivacional", "tristeza", "risa"]:
            filtered_data = [text for text, label in self.train_data if label == choice]
            # Seleccionar al azar una frase de la categoría filtrada
            return random.choice(filtered_data)
        else:
            return "Elección no válida. Por favor, intente de nuevo."

    def generate_and_play(self):
        user_input = self.user_input_entry.get()
        choice = self.model.predict([user_input])[0]

        num_notes = 20  # Número de notas a generar
        min_pitch = 40  # Pitch mínimo de MIDI
        max_pitch = 90  # Pitch máximo de MIDI
        min_duration = 0.5  # Duración mínima de nota (en segundos)
        max_duration = 2.0  # Duración máxima de nota (en segundos)
        self.piano_base(num_notes, min_pitch, max_pitch, min_duration, max_duration)

        # Obtener el texto del prompt basado en la elección del usuario
        prompt = self.get_prompt(choice)

        # Convertir texto a voz
        self.text_to_speech(prompt)

        # Reproducir prompt
        self.play_prompt("prompt.mp3")

        # Reproducir música de fondo
        self.play_music("output.mid")

        # Esperar a que termine la música de fondo antes de reproducir el prompt
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

if __name__ == "__main__":
    root = tk.Tk()
    app = MidiApp(root)
    root.mainloop()
