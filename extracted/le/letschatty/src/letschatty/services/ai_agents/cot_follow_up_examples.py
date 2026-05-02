follow_up_training_examples = [
    {
      "title": "SEND - First Follow-up After Proposal",
      "content": [
        {
          "type": "user",
          "content": "Me interesa el plan premium, ¿me puedes enviar más detalles?"
        },
        {
          "type": "ai",
          "content": "¡Perfecto! Te envío la propuesta completa del plan premium por email con todos los detalles y precios. Incluye todo lo que discutimos: soporte 24/7, integración personalizada y gestor de cuenta dedicado."
        },
        {
          "type": "chain_of_thought",
          "content": "Pasaron 24 horas desde que envié la propuesta y el usuario no ha respondido. Mostró interés explícito pidiendo detalles, así que es apropiado hacer el primer seguimiento para confirmar que recibió la información y ver si tiene preguntas."
        },
        {
          "type": "ai",
          "content": "Hola! ¿Tuviste oportunidad de revisar la propuesta que te envié ayer? Me encantaría conocer tus primeras impresiones y resolver cualquier duda que puedas tener."
        }
      ]
    },
    {
      "title": "SEND - Multi-Follow-up Sequence",
      "content": [
        {
          "type": "user",
          "content": "¿El plan incluye capacitación para mi equipo?"
        },
        {
          "type": "ai",
          "content": "¡Sí! El plan premium incluye 3 sesiones de capacitación online para tu equipo, más acceso a nuestra biblioteca de tutoriales. ¿Te gustaría que programemos la primera sesión para la próxima semana?"
        },
        {
          "type": "chain_of_thought",
          "content": "Pasaron 2 horas desde mi respuesta sobre capacitación y el usuario no respondió a mi pregunta sobre programar la sesión. Es un buen momento para el primer seguimiento."
        },
        {
          "type": "ai",
          "content": "Hola! Vi que te interesa la capacitación incluida. ¿Prefieres que programemos las sesiones para esta semana o la siguiente te viene mejor? También puedo enviarte ejemplos de lo que cubrimos en cada sesión."
        },
        {
          "type": "chain_of_thought",
          "content": "Pasaron 24 horas desde el primer seguimiento y el usuario no respondió. Procedo con el segundo seguimiento, esta vez ofreciendo más valor y opciones flexibles."
        },
        {
          "type": "ai",
          "content": "Hola! Para facilitarte la decisión, te envío un cronograma sugerido de capacitación que funciona bien para equipos como el tuyo. No hay prisa, pero me gustaría saber si hay algún aspecto específico del plan que te gustaría que aclaremos."
        }
      ]
    },
    {
      "title": "SKIP - Customer Needs Weekend to Decide",
      "content": [
        {
          "type": "ai",
          "content": "Te envío la cotización final con el descuento del 15% que acordamos. ¿Qué te parece?"
        },
        {
          "type": "user",
          "content": "Perfecto, me gusta la propuesta. Necesito consultarlo con mi equipo este fin de semana. La semana que viene te confirmo."
        },
        {
          "type": "chain_of_thought",
          "content": "El usuario dio un timeline claro: necesita el fin de semana para consultar con su equipo y confirmará la próxima semana. Debo respetar este cronograma y no presionar. Saltaré este ciclo y programaré para el lunes."
        }
      ]
    },
    {
      "title": "SKIP - Agent Promised Information",
      "content": [
        {
          "type": "user",
          "content": "¿Tienen referencias de clientes similares a mi empresa?"
        },
        {
          "type": "ai",
          "content": "¡Excelente pregunta! Tenemos varios clientes en tu sector. Déjame conseguir casos de estudio específicos que te puedan servir como referencia y te los envío mañana por la mañana."
        },
        {
          "type": "chain_of_thought",
          "content": "Prometí enviar casos de estudio mañana por la mañana. La pelota está en mi cancha, no en la del usuario. No debo hacer seguimiento pidiendo su respuesta cuando soy yo quien debe entregar información. Salto este ciclo."
        }
      ]
    },
    {
      "title": "SUGGEST - High-Value Enterprise Deal",
      "content": [
        {
          "type": "user",
          "content": "Necesitamos una solución para 500 empleados con integración personalizada"
        },
        {
          "type": "ai",
          "content": "Perfecto! Para una implementación de esa escala podemos crear un plan enterprise personalizado. Estaríamos hablando de aproximadamente $50,000 USD anuales con implementación dedicada. ¿Te parece si programamos una llamada con nuestro director comercial?"
        },
        {
          "type": "chain_of_thought",
          "content": "Pasaron 4 horas sin respuesta a una propuesta enterprise de $50,000 para 500 empleados. Este es un deal de alto valor que requiere toque humano y atención personal. Aunque podría enviar un seguimiento automático, esta situación se beneficiaría de la intervención de un agente humano."
        }
      ]
    },
    {
      "title": "SUGGEST - Customer Shows Frustration",
      "content": [
        {
          "type": "user",
          "content": "Es la tercera vez que pregunto por el status de mi solicitud y nadie me da una respuesta clara. Esto es frustrante."
        },
        {
          "type": "ai",
          "content": "Entiendo completamente tu frustración y lamento mucho la experiencia. Voy a escalar tu caso inmediatamente a supervisión para que recibas una respuesta definitiva hoy mismo."
        },
        {
          "type": "chain_of_thought",
          "content": "Pasaron 2 horas desde que escalé el caso y el usuario no ha respondido. Está claramente frustrado por experiencias previas. Esta es una situación delicada que requiere empatía humana y manejo cuidadoso. Un seguimiento automático podría empeorar su percepción del servicio."
        }
      ]
    },
    {
      "title": "SUGGEST - AI Mode is SUGGESTIONS",
      "content": [
        {
          "type": "user",
          "content": "¿Cuánto cuesta el plan básico?"
        },
        {
          "type": "ai",
          "content": "El plan básico tiene un costo de $299 USD mensuales e incluye todas las funcionalidades principales. ¿Te gustaría que programemos una demo para mostrarte exactamente qué incluye?"
        },
        {
          "type": "chain_of_thought",
          "content": "Pasaron 3 horas desde que ofrecí la demo y el usuario no respondió. El modo de IA está configurado en SUGGESTIONS, lo que significa que todos los mensajes deben ser sugeridos a agentes humanos en lugar de enviarse automáticamente. Aunque esta es una situación de seguimiento estándar, debo respetar la configuración del modo."
        }
      ]
    },
    {
      "title": "REMOVE - Customer Requests No Contact",
      "content": [
        {
          "type": "ai",
          "content": "¿Te gustaría recibir información sobre nuestras próximas funcionalidades?"
        },
        {
          "type": "user",
          "content": "No gracias, por favor no me contacten más. No me interesa en este momento."
        },
        {
          "type": "chain_of_thought",
          "content": "El cliente solicitó explícitamente no ser contactado más. Esta es una directiva clara que debo respetar. Continuar con seguimientos sería irrespetuoso y potencialmente dañino para la marca. Debo eliminar todos los seguimientos automáticos inmediatamente."
        }
      ]
    },
    {
      "title": "REMOVE - Deal Successfully Closed",
      "content": [
        {
          "type": "ai",
          "content": "¿Hay algo más que te gustaría saber antes de tomar la decisión?"
        },
        {
          "type": "user",
          "content": "No, está todo claro. Procedo con la compra del plan premium. ¿Me envías el link de pago?"
        },
        {
          "type": "ai",
          "content": "¡Excelente! Te envío el link de pago ahora mismo. Recibirás las credenciales de acceso una vez completado el pago."
        },
        {
          "type": "chain_of_thought",
          "content": "El cliente decidió comprar y está procediendo con el pago. El deal se cerró exitosamente. Ya no hay necesidad de seguimientos de ventas porque se convirtió. La secuencia de seguimiento debe eliminarse y el cliente debe pasar a flujos de customer success."
        }
      ]
    },
    {
      "title": "REMOVE - Maximum Follow-ups Reached",
      "content": [
        {
          "type": "user",
          "content": "Me interesa pero ahora estoy muy ocupado"
        },
        {
          "type": "ai",
          "content": "Entiendo perfectamente. Te dejo mi contacto directo para cuando tengas más tiempo disponible."
        },
        {
          "type": "chain_of_thought",
          "content": "Este fue mi seguimiento #1 hace 48 horas - usuario dijo que está ocupado."
        },
        {
          "type": "ai",
          "content": "Hola! ¿Ya tienes un poco más de tiempo para revisar la propuesta?"
        },
        {
          "type": "chain_of_thought",
          "content": "Seguimiento #2 hace 72 horas - sin respuesta."
        },
        {
          "type": "ai",
          "content": "Esta será mi última comunicación sobre la propuesta. Si en algún momento cambias de opinión o necesitas información, no dudes en contactarme. ¡Que tengas un excelente día!"
        },
        {
          "type": "chain_of_thought",
          "content": "Este fue el seguimiento #3 y final según la estrategia (máximo 3 consecutivos). El usuario no ha respondido a múltiples intentos. Continuar sería comportamiento tipo spam. Debo eliminar la secuencia de seguimiento y dejar que ellos se contacten si se interesan en el futuro."
        }
      ]
    },
    {
      "title": "REMOVE - Deal Lost to Competitor",
      "content": [
        {
          "type": "ai",
          "content": "¿Tuviste oportunidad de comparar nuestra propuesta con otras opciones?"
        },
        {
          "type": "user",
          "content": "Sí, gracias por toda la información. Al final decidimos ir con otra solución que se ajusta mejor a nuestro presupuesto actual."
        },
        {
          "type": "chain_of_thought",
          "content": "El cliente tomó una decisión clara de ir con un competidor. El deal se perdió oficialmente. Continuar con seguimientos sería inapropiado y potencialmente molesto. Debo eliminar graciosamente la secuencia de seguimiento y dejar la puerta abierta para oportunidades futuras."
        }
      ]
    }
  ]
