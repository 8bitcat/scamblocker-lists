# ScamBlocker – listor

`lists.json` hämtas av ScamBlocker-appen varje gång den öppnas:
<https://8bitcat.github.io/scamblocker-lists/lists.json>

Ändrar du filen här uppdateras appen utan en ny appversion. Det tar några minuter innan GitHub
Pages visar den nya filen, och appen läser den nästa gång någon öppnar den.

## Det här går att ändra

**Färdiga spärrar** (`presets`) visas under *New Block → Ready-made block*.

| Fält | Betydelse | Exempel |
|---|---|---|
| `id` | Spärrens id. **Byt aldrig id på en befintlig spärr**: appen följer spärren på id:t, så den som redan lagt till den får de nya serierna automatiskt. | `"dk-mobile"` |
| `name` | Namnet i appen | `"Danish mobile numbers"` |
| `countryCode` | Landskoden utan + | `"45"` |
| `series` | Siffrorna efter landskoden som numren börjar på | `["20", "21", "431"]` |
| `lengths` | Hur många siffror numren har efter landskoden | `[8]` |
| `note` | Förklaringen under namnet | |

En spärr får täcka högst 200 miljoner nummer. Två siffror i en serie med längd 8 blir 1 miljon nummer.

**Meddelande** (`message`) visas överst i appen tills man stänger det. Använd ett nytt `id`
för varje nytt meddelande, annars visas det inte för den som redan har stängt det förra.

```json
"message": { "id": "2026-10-dk", "text": "Danish mobile numbers now include …", "url": "https://…" }
```

Sätt `"message": null` när du inte vill visa något. Ändra också `updated` till dagens datum; det
syns längst ner i appen ("lists 2026-10-19").

## Kontroll

GitHub Actions kör `tools/check.py` vid varje ändring. Blir den röd står felet i loggen. Appen
hoppar över spärrar som inte klarar kontrollen. Om filen inte går att läsa alls behåller appen
den senaste fungerande versionen.
