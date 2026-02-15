const midiInput = document.getElementById('midiInput');
        const inputText = document.getElementById('UploadText');

        midiInput.addEventListener('change', function() {
            if(this.files && this.files.length > 0) {
                inputText.innerText = this.files[0].name;
            } else {
                inputText.innerText = "Select File";
            }
        });

        async function processMidi() {
            const fileInput = midiInput;
            if (!fileInput.files[0]) return alert("Please upload a file first!");

            const reader = new FileReader();
            reader.onload = async (e) => {
                const midi = new Midi(e.target.result);
                let commands = ["scoreboard players add #t music_tick 1"];
                const timeline = {};

                midi.tracks.forEach(track => {
                    track.notes.forEach(note => {
                        const tick = Math.round(note.time * 20) + 1;

                        const channel = track.channel;
                        const instSelect = document.getElementById(`inst-${channel}`) || {value: 'chime'};
                        const volInput = document.getElementById(`vol-${channel}`) || {value: 0.5};

                        const midiNote = note.midi;
                        let adjustedNote = midiNote;
                        while (adjustedNote > 78) adjustedNote -= 12;
                        while (adjustedNote < 54) adjustedNote += 12;

                        const pitch = Math.pow(2, (adjustedNote - 66) / 12);
                        const volume = note.velocity * parseFloat(volInput.value);

                        if (!timeline[tick]) timeline[tick] = [];
                        timeline[tick].push(`execute if score #t music_tick matches ${tick} run playsound minecraft:block.note_block.${instSelect.value} master @a ~ ~ ~ ${volume.toFixed(3)} ${pitch.toFixed(3)}`);
                    });
                });

                const sortedTicks = Object.keys(timeline).sort((a, b) => a - b);
                sortedTicks.forEach(tick => {
                    commands.push(...timeline[tick]);
                });

                document.getElementById('output').value = commands.join('\n');
            };
            reader.readAsArrayBuffer(fileInput.files[0]);
        }

        function copyResult() {
            const copyText = document.getElementById("output").value;
            const copyButton = document.getElementById("copyButton");
            navigator.clipboard.writeText(copyText);
            copyButton.textContent = "Copied!";
            setTimeout(() => {
                copyButton.textContent = "Copy Result";
            }, 2000);
        }
