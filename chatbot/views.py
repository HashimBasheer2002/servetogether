import time
from transformers import pipeline
from django.http import JsonResponse
from django.shortcuts import render

# Set up Hugging Face pipeline for text generation
generator = pipeline("text-generation", model="gpt2", tokenizer="gpt2")

# Knowledge base for disaster-related questions
knowledge_base = {
    "flood": {
        "prevention": [
            "Ensure proper drainage systems are in place to prevent water logging.",
            "Avoid building in flood-prone areas, and maintain green cover to reduce soil erosion.",
            "Regularly clean and inspect drainage systems to avoid blockages.",
            "Educate local communities about flood risks and safety measures."
        ],
        "safety": [
            "In case of a flood, move to higher ground immediately.",
            "Avoid waterlogged areas, and follow evacuation orders promptly.",
            "Stay away from floodwaters and avoid driving through flooded areas.",
            "If caught in a car, stop, stay inside, and avoid moving water."
        ],
        "first_aid": [
            "If someone is injured in a flood, stop any bleeding with clean cloths and keep the person warm.",
            "For drowning cases, perform CPR immediately and call emergency services.",
            "If a person is trapped in floodwaters, keep calm and try to keep their head above water."
        ],
        "post_disaster_care": [
            "After a flood, check for waterborne diseases like cholera or typhoid.",
            "Ensure that drinking water is clean, and avoid consuming contaminated food.",
            "Seek medical attention if any symptoms of illness arise, such as fever or diarrhea.",
            "Follow local government or health organization recommendations for sanitation and vaccination."
        ]
    },
    "earthquake": {
        "prevention": [
            "Earthquake-proof buildings and structures are key to minimizing damage.",
            "Educate citizens on earthquake preparedness drills and emergency responses.",
            "Retrofit old buildings and ensure all new buildings meet earthquake-resistant standards.",
            "Use proper construction materials to improve structural integrity in earthquake-prone areas."
        ],
        "safety": [
            "If indoors, drop to the ground, cover your head and neck, and hold on until shaking stops.",
            "If outside, move to an open area away from buildings, trees, and electrical wires.",
            "If in a car, stop in an open area, away from bridges, underpasses, and overpasses."
        ],
        "first_aid": [
            "For injuries from debris, apply pressure to stop bleeding and immobilize fractures.",
            "Keep the injured person calm, and avoid unnecessary movement to prevent further harm.",
            "For head or neck injuries, avoid movement and keep the person still until help arrives."
        ],
        "post_disaster_care": [
            "Aftershocks may follow the earthquake, so remain alert and stay away from damaged buildings.",
            "Use emergency broadcasts or local news to stay informed of the situation.",
            "If you are in an area of significant destruction, avoid attempting rescues unless trained."
        ]
    },
    "blood_donation": {
        "benefits": [
            "Blood donation helps save lives, improves cardiovascular health, stimulates blood cell production, and can increase longevity in donors.",
            "It’s a simple and quick process that can help those in need during emergencies, particularly after natural disasters."
        ],
        "eligibility": [
            "Donors should be at least 18 years old, weigh 50 kg or more, and be in good health.",
            "They should not have chronic infections or conditions that can be transmitted through blood."
        ],
        "process": [
            "The donation process involves a screening interview, blood collection, and post-donation rest. It typically takes about 30 minutes.",
            "Afterward, most blood centers offer snacks and beverages to help the body recover."
        ],
        "post_donation_care": [
            "After donating blood, drink fluids and avoid heavy exercise for 24 hours.",
            "Rest and avoid alcohol, heavy physical labor, or risky activities for at least 24 hours."
        ]
    },
    "first_aid": {
        "cpr_adult": [
            "For adults, place your hands in the center of the chest, push hard and fast at 100-120 compressions per minute.",
            "Provide rescue breaths every 30 compressions. If possible, use an automated external defibrillator (AED)."
        ],
        "cpr_child": [
            "For children, use one hand for chest compressions and give 2 rescue breaths for every 30 compressions.",
            "Do not attempt CPR on infants under 1 year old unless you have proper training."
        ],
        "burns": [
            "For minor burns, cool the area with running water for 10 minutes.",
            "For severe burns, cover the burn with a clean cloth and seek emergency medical help immediately."
        ],
        "bleeding": [
            "Apply pressure to stop bleeding, elevate the injured limb, and keep the person calm.",
            "If bleeding doesn't stop, seek immediate medical help. For severe bleeding, use a tourniquet above the injury only if necessary."
        ],
        "choking": [
            "For a choking person, perform the Heimlich maneuver or encourage them to cough if they can.",
            "If the airway remains blocked, call emergency services immediately."
        ],
        "heart_attack": [
            "If someone is having a heart attack, call emergency services and have them rest in a comfortable position.",
            "Administer aspirin if available, unless contraindicated, to help prevent further clotting."
        ]
    },
    "disaster_recovery": {
        "psychological_first_aid": [
            "Listen actively to those affected, provide comfort, and avoid overwhelming them with advice.",
            "Encourage them to seek professional mental health support and offer emotional reassurance.",
            "Offer practical help, such as food or shelter, without overwhelming the person."
        ],
        "rescue_teams": [
            "Rescue teams may arrive with specialized equipment like dogs or drones. Always follow their instructions.",
            "Do not attempt rescues on your own unless you have proper training, as it may cause further harm."
        ],
        "volunteering": [
            "You can help by donating blood, offering supplies, or volunteering with local organizations involved in disaster relief efforts.",
            "Be sure to follow safe practices, stay informed, and always prioritize your safety during operations."
        ]
    },
    "safety_measures": {
        "tornado": {
            "safety": [
                "Seek shelter in a basement or an interior room without windows.",
                "Cover yourself with a heavy blanket or mattress to protect from flying debris.",
                "Stay in the shelter until the danger has passed."
            ],
            "preparation": [
                "Ensure your home has a weather radio, emergency kit, and storm shelter plan.",
                "Stay updated with weather alerts during storm season, and keep a flashlight and extra batteries available."
            ]
        },
        "hurricane": {
            "safety": [
                "If you're in the path of a hurricane, evacuate to a safe location.",
                "Avoid floodwaters, stay indoors, and follow official evacuation orders.",
                "Do not return until authorities declare it safe."
            ],
            "preparation": [
                "Prepare for a hurricane by securing your home, having a family evacuation plan, and stocking up on essentials.",
                "Secure windows and doors with storm shutters or plywood."
            ]
        },
        "heatwave": {
            "safety": [
                "Stay hydrated, avoid outdoor activities during peak heat, and stay in air-conditioned spaces.",
                "Wear light clothing, sunscreen, and a hat to protect yourself from the sun."
            ],
            "preparation": [
                "Ensure access to cool spaces, maintain proper hydration, and avoid alcohol or caffeine.",
                "Install fans or air conditioning in living areas. Check on vulnerable family members or neighbors regularly."
            ]
        }
    },
    "rescue_operations": {
        "self_rescue": [
            "If trapped, stay calm and attempt to create noise by banging on pipes or walls.",
            "Use your mobile phone to call for help if possible. Conserve battery power by turning off non-essential apps."
        ],
        "water_rescue": [
            "If trapped in a flood, try to stay on a raised surface and avoid swimming unless absolutely necessary.",
            "Avoid areas with strong currents, and if swept away, try to grab onto a floating object."
        ],
        "earthquake_rescue": [
            "In case of collapsed buildings, look for exit routes, create a safe passage, and alert rescue teams.",
            "Avoid moving debris unless necessary to avoid further injury. Make noise to attract rescuers if you are trapped."
        ]
    },
    "developer": {
        "who_developed": "I was developed by Hashim A. He is a web app developer proficient in Python, Django, HTML, and CSS. He is passionate about disaster management and helping communities during emergencies."
    }
}



MAX_RETRIES = 5  # Maximum retries before giving up


# Function to check the knowledge base first
def search_knowledge_base(query):
    query = query.lower()
    response = None

    # Search the knowledge base for matching topics
    for topic, details in knowledge_base.items():
        if topic in query:
            for key, value in details.items():
                if key in query:
                    response = value
                    break
            if response:
                break

    return response


# Function to handle Hugging Face model request
def ask_huggingface(message, retry_count=0):
    try:
        # Add disaster management instructions to the input message
        context_message = f" Answering:\n\n{message}"

        # Generate a response from the Hugging Face model
        response = generator(context_message, max_length=500, num_return_sequences=1)

        # Extract the text response from the Hugging Face model output
        answer = response[0]['generated_text'].strip()
        return answer
    except Exception as e:
        if retry_count >= MAX_RETRIES:
            return f"Error: {str(e)}. Please try again later."
        print(f"Error: {str(e)}. Retrying {retry_count + 1}/{MAX_RETRIES} in 10 seconds...")
        time.sleep(10)  # Wait for 10 seconds before retrying
        return ask_huggingface(message, retry_count + 1)  # Retry the request with an incremented retry count


def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            # First, search the knowledge base for a response
            knowledge_base_answer = search_knowledge_base(message)

            if knowledge_base_answer:
                # If found, return the answer from the knowledge base
                response = knowledge_base_answer
            else:
                # If not found in the knowledge base, generate a response using Hugging Face model
                response = ask_huggingface(message)

            return JsonResponse({'message': message, 'response': response})
        return JsonResponse({'error': 'No message provided'})

    return render(request, 'chatbot.html')
