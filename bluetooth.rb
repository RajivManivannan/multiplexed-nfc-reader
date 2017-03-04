#!/usr/bin/env ruby

counter = 0
time_interval = 2 # seconds
counter_threshold = 10 # counts
time = (Time.now + time_interval).to_i

FILE_TO_WRITE = "/tmp/bluetooth-zone-id.txt"

uuid_to_machine_zone = {
  "74278BDA-B644-4520-8F0C-720EAF059935" => "Machine A Zone", # CC2541
  "2F234454-CF6D-4A0F-ADF2-F4911BA9FFA6" => "Machine B Zone" # Button Beacon
}

all_reads = {
}

ARGF.each_line do |e|
  _, uuid, _, major, _, minor, _, power, _, rssi = e.split(" ")

  if uuid && major && minor && power && rssi
    all_reads[uuid] = {
      rssi: ((all_reads[uuid] || {})[:rssi] || 0) + rssi.to_i,
      count: ((all_reads[uuid] || {})[:count] || 0) + 1
    }

    counter = counter + 1

    if Time.now.to_i > time || counter == counter_threshold
      counter = 0
      time = (Time.now + time_interval).to_i

      uuid_with_average_rssi = all_reads.reduce({}) do |memo, (group_uuid, reads)|
        memo[group_uuid] = reads[:rssi] / reads[:count]
        memo
      end

      sorted_uuids = uuid_with_average_rssi.sort_by do |uuid, avg_rssi|
        if uuid == "2F234454-CF6D-4A0F-ADF2-F4911BA9FFA6"
          -avg_rssi + 20
        end
        -avg_rssi
      end

      closest_uuid, rssi  = sorted_uuids.first

      all_reads = {}

      File.open(FILE_TO_WRITE, 'w') { |file| file.write(closest_uuid) }
    end
  end
end
