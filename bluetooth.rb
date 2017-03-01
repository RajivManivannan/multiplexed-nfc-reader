#!/usr/bin/env ruby

counter = 0
ten_seconds = 10
time = (Time.now + ten_seconds).to_i

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

    if Time.now.to_i > time || counter == 50
      counter = 0
      time = (Time.now + ten_seconds).to_i

      uuid_with_average_rssi = all_reads.reduce({}) do |memo, (group_uuid, reads)|
        memo[group_uuid] = reads[:rssi] / reads[:count]
        memo
      end

      closest_uuid = uuid_with_average_rssi.sort_by do |uuid, avg_rssi|
        avg_rssi
      end.first.first

      all_reads = {}

      puts "In zone: " + uuid_to_machine_zone[closest_uuid]
    end
  end
end
