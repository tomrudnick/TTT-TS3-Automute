--This function will write all Players to a specific file
function writePlayersToFile(filename, data)
    playerDataString = ""
    for key, value in pairs(data) do
        playerDataString = playerDataString .. value .. "\n"
    end
    file.Write(filename, playerDataString)
end

--This Function is called when something changes with the playerstatus (join, death, alive etc. etc.)
function playerStatus()
    playersAlive = {}
    playersDead = {}
    for k,v in pairs(player.GetAll()) do
        if v:Alive() then
            print("Player :"..v:GetName().." is alive")
            table.insert(playersAlive, v:GetName())
        else
            print("Player :"..v:GetName().." is dead")
            table.insert(playersDead, v:GetName())
        end
    end
    writePlayersToFile("automute/alive.txt", playersAlive)
    writePlayersToFile("automute/dead.txt", playersDead)
end

hook.Add("PlayerSpawn", "SpawnPlayerStatus", playerStatus)
hook.Add("PostPlayerDeath", "PlayerDeathStatus", playerStatus)

print("Automute Script active")

function removeHooks()
    hook.Remove("PlayerSpawn", "SpawnPlayerStatus")
    hook.Remove("PostPlayerDeath", "PlayerDeathStatus")
    file.Write("automute/alive.txt", "")
    file.Write("automute/dead.txt", "")
end

function addHooks()
    hook.Add("PlayerSpawn", "SpawnPlayerStatus", playerStatus)
    hook.Add("PostPlayerDeath", "PlayerDeathStatus", playerStatus)
end

hook.Add("TTTEndRound", "ts3EndMute", removeHooks)
hook.Add("TTTBeginRound", "ts3StartMute", addHooks)

